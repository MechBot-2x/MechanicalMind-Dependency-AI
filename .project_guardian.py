import time


class ProjectGuardian:
    def __init__(self):
        self.blessing = "✨ Que tu código esté libre de bugs y lleno de magia ✨"

    def protect(self):
        print(f"\n{self.blessing}")
        print(f"Protegiendo MechanicalMind AI a las {time.ctime()}\n")


guardian = ProjectGuardian()
guardian.protect()
