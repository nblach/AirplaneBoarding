import csv

with open('out_test.txt', mode='w') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(['Method', 'Boarding Time 1'])

print('done')
