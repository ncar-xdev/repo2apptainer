from pkg_resources import DistributionNotFound, get_distribution

try:
    version = get_distribution('repo2singularity').version
except DistributionNotFound:  # pragma: no cover
    version = '0.0.0'  # pragma: no cover
