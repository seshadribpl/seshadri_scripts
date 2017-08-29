class animal:
  def walk(self,stunt):
    self.stunt = stunt
    print 'walking' 
    print 'the stunt is %s' %self.stunt


giraffe = animal()
giraffe.walk('jumping')

