#!/usr/bin/env python
import sys
import re

raw_number = str(input('Enter a number: '))




print(raw_number)

# number_without_commas =  re.sub("\D", "", raw_number)




if ',' in raw_number:
    number_without_commas = raw_number.replace(',', '')
    # print('number without commas: %s' %number_without_commas)

else:
    number_without_commas = raw_number

# print(number_without_commas)



if not number_without_commas.isdigit():
    print('not a number')
    sys.exit(-1)





else:
    number_without_commas = raw_number

# print(number_without_commas)



number_len = len(raw_number)


if number_len < 4:
        print('The number %s is less than 4 digits long; no need for commas' %number_without_commas)
        sys.exit(0)
        
def convert_to_intl(number):

    reversed_number = ''.join(reversed(number))

    reversed_number_with_commas = (re.sub(r'(...)', r'\1,', reversed_number))
    
    converted_number_with_commas = ''.join(reversed(reversed_number_with_commas))
    if converted_number_with_commas[0] == ',':
        number_with_leading_comma_removed = converted_number_with_commas[1:]
        print('the number in the international system is: %s' %number_with_leading_comma_removed)
    else:
        print ('the number in the international system is: %s' %converted_number_with_commas)

def convert_to_indian(number):



    reversed_number = ''.join(reversed(number))
    # print('the reversed number is: %s' %reversed_number)

    # Break up the reversed number into two parts

    last_three_digits = number[-3:]
    # print('the last three digits are: %s' %last_three_digits)

    
    part_2_reversed = reversed_number[3:]

    # print('part_1_reversed is: %s' %part_1_reversed)
    # print('part_2_reversed is: %s' %part_2_reversed)

    # Now add commas to part2

    reversed_part_2_with_commas = (re.sub(r'(..)',r'\1,', part_2_reversed))
    # print(reversed_part_2_with_commas)

    converted_part_2_with_commas =  ''.join(reversed(reversed_part_2_with_commas))
    # print(converted_part_2_with_commas)

    if converted_part_2_with_commas[0] == ',':
        converted_part_2_with_leading_comma_removed = converted_part_2_with_commas[1:]
        # print(converted_part_2_with_leading_comma_removed)

    converted_number = converted_part_2_with_leading_comma_removed + ',' + last_three_digits

    print('the converted number in the Indian system is: %s' %converted_number)

    


if __name__ == '__main__':
    
    convert_to_indian(number_without_commas)
    convert_to_intl(number_without_commas)

