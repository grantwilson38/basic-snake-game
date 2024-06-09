class Level:
    def __init__(self):
        self.level = 1
        self.miniboss = None

    def increase(self):
        self.level += 1

    def reset(self):
        self.level = 1

    def draw(self, screen, font):
        level_surface = font.render(f"Level: {self.level}", True, (255, 255, 255))
        screen.blit(level_surface, (500, 30))