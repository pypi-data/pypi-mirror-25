"""이 파일은 nester.py 모듈이며,priny_lol()함수 하나를 제공합니다
이함수는 포함된 리스트가 있을 경우 그것을 포함해서 리스트의 모든 항목을
출력합니다.  """

def print_lol(the_list,level=0):
  for each_item in the_list:
      if isinstance(each_item,list):
          print_lol(each_item,level+1)
      else:
          for num in range(level):
                  print("\t",end='')
          print(each_item)
