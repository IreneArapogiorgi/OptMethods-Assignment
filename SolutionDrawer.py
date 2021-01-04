import matplotlib.pyplot as plt

class SolDrawer:
    @staticmethod
    def draw(it, sol, nodes):
        plt.clf()
        SolDrawer.drawPoints(nodes)
        SolDrawer.drawRoutes(sol)
        plt.savefig(str(it))

    @staticmethod
    def drawPoints(nodes:list):
        x = []
        y = []
        for i in range(len(nodes)):
            n = nodes[i]
            x.append(n.x)
            y.append(n.y)
        plt.scatter(x, y, c="blue")

    @staticmethod
    def drawRoutes(sol):
        if sol is not None:
            for route in sol.routes:
                for i in range(0, len(route) - 1):
                    c0 = route[i]
                    c1 = route[i + 1]
                    plt.plot([c0.x, c1.x], [c0.y, c1.y], c="black")