class cartoon:
    def __init__(self,name,show,catchphore):
        self.name = name
        self.show = show
        self.catchphore = catchphore
    def introduction_fu(self):
        print( f"hello my name is {self.name}")
    def speak(self):
        print(f"{self.name}says{self.catchphore}")
Tom = cartoon("harshit","Xyz","yzx")
Tom.introduction_fu()