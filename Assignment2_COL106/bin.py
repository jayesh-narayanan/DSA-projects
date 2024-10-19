class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id=bin_id
        self.capacity=capacity
        self.objects=[]
        self.size=0

    def add_object(self, object):
        self.objects.append(object.object_id)
        self.size+=1

    def remove_object(self, object_id):
        for i in range(self.size):
            if (self.objects[i]==object_id):
                del self.objects[i]
                self.size-=1
                break

