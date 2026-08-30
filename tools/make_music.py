#!/usr/bin/env python3
"""
Generates the ambient harp loop shipped with the invitation.
Original synthesis - nothing sampled, nothing licensed.
Swap assets/music.mp3 for any other track and nothing else changes.
"""
import numpy as np, subprocess, os

SR = 44100
DUR = 48.0
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
rng = np.random.default_rng(4)

n = int(SR * DUR)
t = np.arange(n) / SR
left = np.zeros(n)
right = np.zeros(n)


def note(freq, start, dur, amp, pan=0.5, bright=1.0):
    """One plucked harp note: a few detuned partials under an exponential decay."""
    i0 = max(int(start * SR), 0)
    ln = int(dur * SR)
    if i0 >= n:
        return
    ln = min(ln, n - i0)
    tt = np.arange(ln) / SR
    env = np.exp(-tt * (2.6 / dur * 1.5))
    env *= 1 - np.exp(-tt * 420)                      # soft attack
    sig = np.zeros(ln)
    for k, w in ((1, 1.0), (2, .38 * bright), (3, .17 * bright),
                 (4, .08 * bright), (6, .03 * bright)):
        detune = 1 + (k - 1) * 0.0008
        sig += w * np.sin(2 * np.pi * freq * k * detune * tt +
                          rng.uniform(0, 6.28))
    sig *= env * amp
    left[i0:i0 + ln] += sig * (1 - pan)
    right[i0:i0 + ln] += sig * pan


def pad(freqs, start, dur, amp):
    """A warm sustained bed under the harp."""
    i0 = max(int(start * SR), 0)
    ln = min(int(dur * SR), n - i0)
    if ln <= 0:
        return
    tt = np.arange(ln) / SR
    env = np.sin(np.pi * tt / (ln / SR)) ** 2
    sig = np.zeros(ln)
    for f in freqs:
        for k, w in ((1, 1.0), (2, .22), (3, .08)):
            lfo = 1 + .0016 * np.sin(2 * np.pi * (0.13 + 0.02 * k) * tt)
            sig += w * np.sin(2 * np.pi * f * k * lfo * tt + rng.uniform(0, 6.28))
    sig *= env * amp / len(freqs)
    left[i0:i0 + ln] += sig * .5
    right[i0:i0 + ln] += sig * .5


def hz(semitones_from_a4):
    return 440.0 * 2 ** (semitones_from_a4 / 12)


# F major pentatonic, warm and open: F G A C D
SCALE = [hz(s) for s in (-16, -14, -12, -9, -7, -4, -2, 0, 3, 5, 8, 10, 12)]
BASS = [hz(s) for s in (-28, -26, -23, -21)]

# ── the arpeggio: a slow rising-and-falling figure ──────────────
step = 0.42
idx = 0
pos = 0.0
direction = 1
while pos < DUR:
    f = SCALE[idx % len(SCALE)]
    accent = 1.0 if idx % 4 else 1.35
    note(f, pos, 3.4, 0.15 * accent,
         pan=0.5 + 0.28 * np.sin(idx * 0.7), bright=0.9)
    if idx % 8 == 0:                                   # a low anchor note
        note(BASS[(idx // 8) % len(BASS)], pos, 5.0, 0.13, pan=.5, bright=.5)
    if idx % 6 == 3:                                   # sparkle an octave up
        note(f * 2, pos + step * .5, 2.2, 0.055, pan=0.5 - 0.3 * np.sin(idx))
    idx += direction
    if idx >= len(SCALE) - 1 or idx <= 0:
        direction *= -1
        idx = max(0, min(idx, len(SCALE) - 1))
    pos += step

# ── chord bed ───────────────────────────────────────────────────
CHORDS = [(-16, -12, -9), (-14, -9, -5), (-21, -16, -12), (-19, -14, -10)]
for i in range(int(DUR // 6) + 1):
    ch = CHORDS[i % len(CHORDS)]
    pad([hz(s) for s in ch], i * 6 - 0.5, 8.0, 0.10)

# ── a short, soft room reverb (FFT convolution) ─────────────────
ir_len = int(SR * 1.5)
ir_t = np.arange(ir_len) / SR
ir = rng.normal(0, 1, ir_len) * np.exp(-ir_t * 4.2)
ir[0] = 1.0
ir /= np.abs(ir).sum() / 2.6

def conv(sig):
    m = 1
    while m < len(sig) + ir_len:
        m *= 2
    out = np.fft.irfft(np.fft.rfft(sig, m) * np.fft.rfft(ir, m), m)[:len(sig)]
    return out

left  = 0.68 * left  + 0.42 * conv(left)
right = 0.68 * right + 0.42 * conv(right)

# ── make it loop: crossfade the tail into the head ──────────────
xf = int(SR * 3.0)
fade = np.linspace(0, 1, xf)
for ch in (left, right):
    ch[:xf] = ch[:xf] * fade + ch[-xf:] * (1 - fade)
left, right = left[:-xf], right[:-xf]

stereo = np.stack([left, right], axis=1)
stereo /= np.max(np.abs(stereo)) + 1e-9
stereo *= 0.82
# gentle soft-clip for warmth
stereo = np.tanh(stereo * 1.15) / np.tanh(1.15)

pcm = (stereo * 32767).astype('<i2')
raw = os.path.join(OUT, "_music.raw")
pcm.tofile(raw)

mp3 = os.path.join(OUT, "music.mp3")
subprocess.run(["ffmpeg", "-y", "-v", "error",
                "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", raw,
                "-c:a", "libmp3lame", "-b:a", "112k", mp3], check=True)
os.remove(raw)
print("music.mp3  %.1f s  %.0f KB" % (len(left) / SR, os.path.getsize(mp3) / 1024))
