
import io
import os
import sys
import nbformat

def nbgen(infilename, outfilename):

    nb = nbformat.read(infilename,  as_version=4)

    for i in range(len(nb.cells)):

        if nb.cells[i].cell_type == 'code':

            ##
            ## borra la numeración
            ##
            nb.cells[i].execution_count = None

            ##
            ## borra la salida
            ##
            if len(nb.cells[i].outputs) != 0:

                nb.cells[i].outputs = []

            ##
            ## borra el codigo de solucion
            ##
            if len(nb.cells[i].source) != 0:

                source_in  = nb.cells[i].source.splitlines()
                source_out = []

                is_ok = True


                for j in range(len(source_in)):

                    if source_in[j].strip() == '###__begin__':

                        is_ok = False

                    if is_ok == True:

                        source_out.append(source_in[j])

                    if source_in[j].strip() == '###__end__':

                        is_ok = True
                #
                #
                #
                if source_out != []:

                    nb.cells[i].source = ['\n'.join(source_out)]

                else:

                    nb.cells[i].source = []


    nbformat.write(nb, outfilename)

if __name__ == '__main__':
    ##
    nbgen(infilename = sys.argv[1], outfilename = sys.argv[2])
    ##
