import timeit
from collections import Counter
from time import perf_counter_ns

from hashmod import compute_hash


def main():
    class MyBlog:
        ...

    MCACHE_SIZE_EXP = 12
    attr_names = [f'post{i}' for i in range((1 << MCACHE_SIZE_EXP) + 1)]
    hash_list = [compute_hash(MyBlog, name) for name in attr_names]
    hash_counts = Counter(hash_list).most_common()

    h0 = hash_counts[0][0]
    idx = hash_list.index(h0)
    name_ref = attr_names[idx]

    idx = hash_list.index(h0, idx+1)
    name_coll = attr_names[idx] 

    h1 = hash_counts[1][0]
    idx = hash_list.index(h1)
    name_noncoll = attr_names[idx]
   
    for name in (name_ref, name_coll, name_noncoll):
        setattr(MyBlog, name, None)

    stmt_collision = f"""
MyBlog.{name_ref}
MyBlog.{name_coll}
    """

    stmt_no_collision = f"""
MyBlog.{name_ref}
MyBlog.{name_noncoll}
    """

    kwargs = dict(
        timer=perf_counter_ns,
        repeat=20,
        number=1_000_000,
        globals=dict(MyBlog=MyBlog)
    )

    for stmt in (stmt_collision, stmt_no_collision):
        timings = timeit.repeat(stmt, **kwargs)
        avg_time = sum(timings) / len(timings) / kwargs['number'] / 2
        print(f'{avg_time:.2f} ns')


if __name__ == '__main__':
    main()
