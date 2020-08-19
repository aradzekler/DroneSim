class PyGameObjectInterface:
    def update_all(self,elements):
        for element in elements:
            element.update()
        

    # TODO: limit movement (drone get stuck in walls)
    # displaying the screen.
    def display_all(self,elements):
        for element in elements:
            element.display()


    def update(self):
        """Udpate objects"""
        pass


    def display(self):
        """render objects"""
        pass