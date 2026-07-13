# Reviewer response templates

## R1. “Frequency hopping USBL already exists.”

Yes. We do not claim the first use of frequency hopping in USBL. Prior work has used frequency-hopped
acoustic modem sequences and Costas-like waveform diversity for underwater positioning. Our claim is
narrower: we identify a carrier-locked coherent multipath DOA-bias component that remains after
direct-path gating, and use ping-to-ping carrier agility to whiten that residual before TOA/TDOA/DOA
fusion in a UKF tracking loop.

## R2. “How is this different from Nhat et al. Costas hopping USBL?”

Nhat et al. use an intra-ping Costas waveform to sharpen correlation peaks and improve time-delay /
ranging precision in shallow-water USBL. In contrast, our schedule changes the carrier across pings.
The target error is not the TOA peak width but the temporal correlation of DOA elevation bias caused by
in-gate coherent surface-reflection leakage. The tested effect is therefore residual whitening and
static 600 m tracking RMSE reduction, not baseline optimization or time-delay variance reduction.

## R3. “How is this different from Qian et al. frequency-comb iUSBL?”

Frequency-comb iUSBL uses coherent multi-frequency signals for integrated positioning and communication.
Its system goal is spectral efficiency, ranging, and autonomous iUSBL functionality. Our method does not
introduce a comb waveform or communication integration. It uses a frozen ping-to-ping carrier schedule
to rotate the direct/reflected interference phase and reduce the temporal correlation of post-gating DOA
bias in a compact USBL tracking loop.

## R4. “Isn’t this just radar glint frequency agility?”

The radar analogy is real and is cited. Frequency agility has long been used to decorrelate angular
glint-like errors. The contribution here is not the abstract principle but its mechanism-level
translation to shallow-water USBL: an in-gate surface-reflection component creates a carrier-locked DOA
bias after direct-path gating. We validate this mechanism in a TOA/TDOA/DOA-UKF localization pipeline
and quantify the static/moving boundary.

## R5. “Why no moving-target RMSE improvement?”

The moving-target result is intentionally reported as a boundary. Carrier agility strongly whitens the
moving-target elevation residual, but the target motion already changes the path-difference term
`delta(t)`, producing motion-induced self-whitening under the fixed carrier. In some geometries the
additional hopping can also increase tail risk. Therefore, the validated performance claim is static
and very-slow-drift long-range tracking, not general moving-target localization.

## R6. “Does the method remove multipath?”

No. It mitigates one carrier-locked coherent residual component that survives direct-path gating. It
does not remove all multipath, and it does not change the compact-aperture geometry floor. This is why
the 600 m RMSE remains meter-scale even after improvement.
