from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "94. Manuscript v3" / "manuscript_draft_v3.md"
OUT = Path(__file__).resolve().parent / "manuscript_draft_v4_refs.md"


REFERENCE_SECTION = """## References

- J. M. Loomis and E. R. Graf, "Frequency-Agility Processing to Reduce Radar Glint Pointing Error," *IEEE Transactions on Aerospace and Electronic Systems*, vol. AES-10, no. 6, pp. 811--820, 1974, doi: 10.1109/TAES.1974.307889.
- R. Delano, "A Theory of Target Glint or Angular Scintillation in Radar Tracking," *Proceedings of the IRE*, vol. 41, no. 12, pp. 1778--1784, 1953, doi: 10.1109/JRPROC.1953.274368. *(Optional radar-glint background reference.)*
- P.-P. J. Beaujean, A. I. Mohamed, and R. Warin, "Acoustic positioning using a tetrahedral ultrashort baseline array of an acoustic modem source transmitting frequency-hopped sequences," *The Journal of the Acoustical Society of America*, vol. 121, no. 1, pp. 144--157, 2007, doi: 10.1121/1.2400616.
- H. B. Nhat, L. V. Hai, G. T. Quang, D. N. Van, H. V. Le, and T. T. Xuan, "Optimizing baseline in USBL using Costas hopping to increase navigation precision in shallow water," in *2022 16th International Conference on Ubiquitous Information Management and Communication (IMCOM)*, pp. 1--6, 2022, doi: 10.1109/IMCOM53663.2022.9721736.
- Z. Qian, S. Liu, Y. Zhu, and X. Fu, "Integrated Acoustic Frequency Comb Signal for Underwater Inverted Ultrashort Baseline Autonomous Positioning Systems," *IEEE Internet of Things Journal*, vol. 12, no. 14, pp. 27628--27637, 2025, doi: 10.1109/JIOT.2025.3564346.
"""


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    text = text.replace(
        "> Draft v3 (2026-07-10). Integrates the v2 manuscript (folder 92) with the method/protocol\n"
        "> code-audit patches from folder 93. Citation placeholders remain pending the folder-86 audit\n"
        "> and are marked as `[..._REF]`.",
        "> Draft v4-ref (2026-07-10). Starts from manuscript v3 (folder 94) and replaces the main\n"
        "> citation placeholders using the metadata-closed references from folder 96.",
    )
    replacements = {
        "[RADAR_FREQ_AGILITY_REF]": "[Loomis1974FrequencyAgilityGlint]",
        "[FH_USBL_REF]": "[Beaujean2007FrequencyHoppedUSBL]",
        "[COSTAS_USBL_REF]": "[Nhat2022CostasUSBL]",
        "[FREQ_COMB_REF]": "[Qian2025FrequencyCombIUSBL]",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    marker = "\n## References"
    idx = text.find(marker)
    if idx == -1:
        raise RuntimeError("References section not found")
    text = text[:idx] + "\n" + REFERENCE_SECTION
    OUT.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

