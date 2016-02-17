import sys, getopt

def user_help():

    sys.stdout.write("\n\n\nCommand line arguments must be entered in the following format, using all specifiers:\n\n")
    sys.stdout.write("  -f   <FASTA filename>            \n")


def parsing():

    filename = None # Name of FASTA file
    chromo = None # Chromosome name in the FASTA file
    kmer_size = None # size of k-mer to search for

    # Getting the arguments from the user
    try:
        options, remainder = getopt.getopt(sys.argv[1:],"f:", ["help"])

    # An error ends the program and displays the help comments
    except getopt.GetoptError:
        sys.stdout.write("\n\n\nArguments were not entered correctly.")
        user_help()
        sys.exit(1)

    # Processing the list of arguments from 'getopt'
    for op, value in options:
        if op=="-f":
            filename = value
            print "\n"
        elif op=="--help":
            user_help()
        else:
            sys.stdout.write("Unhandled argument: [%s][%s]" % (op))

    # The user must enter all arguments or the program is stopped
    if filename == None:
        sys.stdout.write("\n\n\nNot all arguments were specified.")
        user_help()
        sys.exit(1)

    return filename


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    #print '\n'
    return previous_row[-1]

def create_matrix(seq):

    seq1 = seq[0]
    seq2 = seq[1]

    Matrix = [[0 for x in range(len(seq1)+1)] for x in range(len(seq2)+1)]

    #initialize column 1
    for i in range(len(seq2)+1):
        Matrix[i][0] = i
    #initialize row 1
    for j in range(len(seq1)+1):
        Matrix[0][j] = j

    for i in range(1, len(seq1)+1):
        for j in range(1, len(seq2)+1):
            top = Matrix[i][j-1]
            left = Matrix[i-1][j]
            diag = Matrix[i-1][j-1]

            Matrix[i][j] = min((diag + subst_score(seq1[i-1], seq2[j-1])), left + 1, top + 1)

    print_Matrix(Matrix)


def subst_score(A, B):
    score = 0
    if A == B:
        score = 0
    else:
        score = score + 1

    return score






def print_Matrix(matrix):
    for i in matrix:
        print i

def read_fasta_file(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    sequence = ''
    sequences = []
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith('>') == False:                   #Add to sequence if the line doesn't start with '<'
            sequence += line.strip()
            if i == len(lines) -1:
                sequences.append(sequence)
                break
        else:
            if sequence:
                sequences.append(sequence)
            sequence = ""
    return sequences

if __name__ == '__main__':
    filename = parsing()
    seq = read_fasta_file(filename)
    create_matrix(seq)
    length = len(seq)
    for i in range(0, length, 2):
        edit_distance = levenshtein(seq[i],seq[i+1])
        print edit_distance