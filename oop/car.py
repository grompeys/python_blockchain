from vehicle import Vehicle


class Car(Vehicle):
    # top_speed = 1000
    # warnings = []

    def brag(self):
        print('Look how cool!')

car1 = Car()
car1.drive()
car1.add_warning('New warning')
print(car1.get_warnings())
# car1.warnings.append('Test')
print(car1.__dict__)

car2 = Car(2000)
car2.drive()