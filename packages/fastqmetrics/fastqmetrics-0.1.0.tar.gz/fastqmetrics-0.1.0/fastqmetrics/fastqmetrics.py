from nanoget import stream_fastq_full
from argparse import ArgumentParser
from fastqmetrics.version import __version__


def main():
    args = get_args()
    print("{}".format('\t'.join(['readname', 'length', 'averageQ', 'medianQ'])))
    for res in stream_fastq_full(args.fastq, args.threads):
        print("{}".format("\t".join((str(i) for i in res))))


def get_args():
    parser = ArgumentParser(description="Extract metrics from a fastq file, streaming")
    parser.add_argument("-v", "--version",
                        help="Print version and exit.",
                        action="version",
                        version='fastqmetrics {}'.format(__version__))
    parser.add_argument("-t", "--threads",
                        help="Set the allowed number of threads to be used by the script. \
                        This only applies to bam and fastq format as data source",
                        default=4,
                        type=int)
    parser.add_argument("fastq",
                        help="Fastq file to extract features from.")
    return parser.parse_args()


if __name__ == '__main__':
    main()
