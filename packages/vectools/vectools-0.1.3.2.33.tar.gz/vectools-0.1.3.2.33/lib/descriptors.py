from collections import OrderedDict
from itertools import product


class NComposition:

    def __init__(self, kmer_len, alphabet):
        """
        :param kmer_len: An integer must be greater than zero.
        :param alphabet: A list of characters to use for alphabet.
        """
        # Generate sorted n-composition vectors.
        self.kmer_len = kmer_len
        self.kmer_list = sorted([''.join(kmer) for kmer in product(alphabet, repeat=kmer_len)])

    def calculate(self, sequence):
        """ This function calculates the n-composition of a sequence within a given alphabet.
        :param sequence:
        :param return_string:
        :return:
        """
        output_vec = []
        seq_len = len(sequence) - self.kmer_len + 1
        for kmer in self.kmer_list:
            output_vec.append(float(sequence.count(kmer)) / seq_len )

        # Count the number of possible positions within the alphabet.
        # @TODO: Should we add a check to make sure all alphabet els are the same len?
        # sequence_list = [
        # sequence[i:i + len(self.alphabet_list[0])] for i in range(len(sequence) - (len(self.alphabet_list[0]) - 1))]
        #seq_len = len(sequence)
        # Split up the sequence into k-mers moving +1 each time until the end of the sequnece minsu the kmer len.
        #sequence_list = []
        #for i in range(seq_len - (self.kmer_len - 1)):
        #    sequence_list.append(sequence[i:i + self.kmer_len])
        #descriptor_vec = []
        #for kmer in self.alphabet_list:
        #    vec_el = float(sequence_list.count(kmer)) / seq_len
        #    descriptor_vec.append(vec_el)

        return output_vec

    def getcoltitles(self):
        """
        :return: The column ids of the feature calculated.
        """
        return self.kmer_list


class Transition:
    """ Supporting k-mers will make vectors unreasonably large, therefore k-mers not supported at this time.
    """

    def __init__(self, alphabet, kmer_len, sum_transitions=False):
        """ Here we make a list of all transition junctions i.e. where a transition takes place.
        Therefore, to find the transitions all we need to do is count the transition junctions.
        :param alphabet:
        :param kmer_len:
        :param sum_transitions
        """
        self.transitions_list = []
        self.junction_len = kmer_len * 2
        self.sum_transitions = sum_transitions
        alphabet_list = sorted([''.join(kmer) for kmer in product(alphabet, repeat=kmer_len)])
        for i in alphabet_list:
            for j in alphabet_list:
                if i != j:
                    self.transitions_list.append(i+j)

    def calculate(self, sequence):
        """ As non-transition bases were filtered in the previous example.
        :param sequence:
        :return:
        """
        junction_list = []
        junction_sum = 0
        possible_junctions = len(sequence) - self.junction_len + 1

        # Count transitions
        for junction in self.transitions_list:
            junction_cnt = sequence.count(junction)
            junction_list.append(float(junction_cnt) / possible_junctions)
            junction_sum += junction_cnt

        # Determine which type of vector to output.
        if self.sum_transitions:
            output_vec = [junction_sum / possible_junctions]
        else:
            output_vec = junction_list

        return output_vec

    def getcoltitles(self):
        """
        :return: The column ids of the feature.
        """
        if self.sum_transitions:
            col_titles_list = ["total_%s-mer_transitions" % int(self.junction_len / 2)]
        else:
            col_titles_list = [self.transitions_list]
        return col_titles_list


class Gapped:

    def __init__(self, kmer_len, alphabet, round_to, allow_nonstandard=True):
        pass

    def calculate(self, sequence, start_len, stop_len):

        return None

    def getcoltitles(self):
        """
        :return: The column ids of the feature.
        """
        return self.col_titles


class GroupedPropertiesNComposition:

    def __init__(self, groups, kmer_len=2):
        """ Initialize two variables
        :param groups: A special type of vector
        """

        # Make a basic sets of data
        group_set = set()
        motif_dict = dict()

        initial_group_list = []

        for line in open(groups):
            group, motif = line.strip().split()
            initial_group_list.append([group, motif])

        # Copy initial_group_list.
        kmer_group_list = list(initial_group_list)
        new_list = []
        for k in range(kmer_len-1):
            for row_i in range(len(kmer_group_list)):
                for row_j in range(len(initial_group_list)):
                    new_group = kmer_group_list[row_i][0] + initial_group_list[row_j][0]
                    new_motif = kmer_group_list[row_i][1] + initial_group_list[row_j][1]
                    new_list.append([new_group, new_motif])
            kmer_group_list = list(new_list)

        for group, motif in kmer_group_list:
            group_set.add(group)
            # Make a dictionary of sets with the motifs as keys and a set of groups as the value.
            # This allows for motifs to exist within multiple groups.
            if motif not in motif_dict:
                motif_dict[motif] = set()
            motif_dict[motif].add(group)

        self.groups = sorted(group_set)
        self.motif_dict = OrderedDict((motif, motif_dict[motif]) for motif in sorted(motif_dict))

    def calculate(self, sequence):
        # Make a temporary place to store output data,
        groups_vector_dict = {group: 0 for group in self.groups}
        seq_len = len(sequence)
        for motif in self.motif_dict:
            tmp_motif_cnt = sequence.count(motif)
            for group in self.motif_dict[motif]:
                groups_vector_dict[group] += tmp_motif_cnt

        # Do this step one all addition has been performed as division is a lossy operation.
        groups_vector = []
        for group in self.groups:
            groups_vector.append(float(groups_vector_dict[group]) / seq_len)

        return groups_vector

    def get_column_titles(self):
        return self.groups
