#!/usr/bin/env python
"""
eval.py
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import dcargs
from rich.console import Console

from nerfstudio.utils.eval_utils import eval_setup

console = Console(width=120)

logging.basicConfig(format="[%(filename)s:%(lineno)d] %(message)s", level=logging.INFO)


@dataclass
class ComputePSNR:
    """Load a checkpoint, compute some PSNR metrics, and save to a JSON."""

    # Path to config YAML file.
    load_config: Path
    # Name of the output file.
    output_path: Path = Path("output.json")

    def main(self) -> None:
        """Main function."""
        config, pipeline, checkpoint_path = eval_setup(self.load_config)

        assert self.output_path.suffix == ".json"
        metrics_dict = pipeline.get_average_eval_image_metrics()
        # save output to some file
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        benchmark_info = {
            "experiment_name": config.experiment_name,
            "method_name": config.method_name,
            "checkpoint": str(checkpoint_path),
            "results": metrics_dict,
        }
        self.output_path.write_text(json.dumps(benchmark_info, indent=2), "utf8")
        console.print(f"Saved results to: {self.output_path}")


def entrypoint():
    """Entrypoint for use with pyproject scripts."""
    dcargs.extras.set_accent_color("bright_yellow")
    dcargs.cli(ComputePSNR).main()


if __name__ == "__main__":
    entrypoint()

# For sphinx docs
get_parser_fn = lambda: dcargs.extras.get_parser(ComputePSNR)  # noqa
