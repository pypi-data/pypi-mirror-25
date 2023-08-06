import argparse
import os


def create_group(args):
    g = open(args.group, 'w')
    g.write('\t'.join(args.sample))
    g.close()
    return g


def add_sample(args):
    g = open(args.group, 'a')
    g.write('\t'+'\t'.join(args.samples))
    g.close()


def rem_sample(args):
    samples = open(args.group).readlines()
    for sample in args.samples:
        samples.remove(sample)
    g = open(args.group, 'w')
    g.write('\t'.join(samples))
    g.close()


def show_group(args):
    samples = open(args.group).readline().split()
    for sample in samples:
        print(sample)


def delete_group(group):
    os.remove(group)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="subcommands")
    create_parser = subparsers.add_parser("create", help="create a new group")
    add_parser = subparsers.add_parser("add", help="add a sample to a group")
    rem_parser = subparsers.add_parser("remove", help="remove a sample from a \
                                                       group")
    show_parser = subparsers.add_parser("show", help="shows all samples \
                                                      contained in a group")
    create_parser.add_argument("group")
    create_parser.add_argument("sample", nargs='+')
    add_parser.add_argument("group")
    add_parser.add_argument("sample", nargs='+')
    rem_parser.add_argument("group")
    rem_parser.add_argument("sample")
    show_parser.add_argument("group")
    create_parser.set_defaults(func=create_group)
    add_parser.set_defaults(func=add_sample)
    rem_parser.set_defaults(func=rem_sample)
    show_parser.set_defaults(func=show_group)

    args = parser.parse_args()
    args.func(args)
