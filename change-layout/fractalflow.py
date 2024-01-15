from metaflow import step, FlowSpec, current, card, pypi, profile
from metaflow.cards import Markdown, ProgressBar, Image

import random
import time


class FractalFlow(FlowSpec):
    def generate_fractal(self, seed):
        import pyfracgen as pf
        from matplotlib import colormaps

        xbound = (2.5, 3.4)
        ybound = (3.4, 4.0)
        res = pf.lyapunov(
            seed, xbound, ybound, width=4, height=3, dpi=250, ninit=2000, niter=500
        )
        img, _ = pf.images.markus_lyapunov_image(
            res, colormaps["GnBu"], colormaps["GnBu_r"], gammas=(8, 1)
        )
        return img

    @pypi(packages={"pyfracgen": "0.1.0"}, python="3.11.7")
    @card(type="blank")
    @step
    def start(self):
        progress = ProgressBar(max=5, label="Fractals generated")
        current.card.append(progress)
        for i in range(6):
            seed = "".join(random.choice("AB") for i in range(8))
            progress.update(i)
            caption = Markdown(f"# Generating {seed}...")
            current.card.append(caption)
            current.card.refresh()
            t = time.time()
            frac = self.generate_fractal(seed)
            n = int(1000 * (time.time() - t))
            caption.update(f"# Fractal {seed} took {n} ms")
            current.card.append(Image.from_matplotlib(frac))
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    FractalFlow()
