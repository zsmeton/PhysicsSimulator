import GUI
import pygame as pg

pg.init()
screen = pg.display.set_mode((640, 480))


def main():
    clock = pg.time.Clock()
    input_box1 = GUI.InputBox(100, 100, 140, 32)
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            input_box1.handle_event(event)

        input_box1.update()

        screen.fill((30, 30, 30))
        input_box1.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()
