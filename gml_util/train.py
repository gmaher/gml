def train(train_step, dataset, iterations, loggers, print_every=1000):
    for i in range(iterations):
        x = dataset.next()
        train_step(x)
        if i%print_every == 0:
            print("Iteration {}".format(i))

            for log in loggers:
                log.log(i)
