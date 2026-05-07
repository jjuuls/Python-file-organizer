name =  input('Enter your name: ' )
age = int(input('Enter your age: '))

years_until_100 = 100 - age

if age > 18:
    print(f'{name}, you are an adult.')
else:
    print(f'{name} you are a minor.')
