import matplotlib.pyplot as plt
import numpy as np
import math


def figure1_paper_model_vs_our_model(labels, boarding_data, n, m):
    old_data = [24.69, 27.74, 28.56, 29.80, 31.35, 30.66, 31.02, 33.77, 31.43, 30.78, 32.51, 39.80, 34.73, 29.59, 27.42,
                25.01, 27.91, 29.60, 28.30, 26.50, 29.27, 30.36, 24.75, 26.28, 25.80, 35.64, 27.23, 26.91, 50.67, 41.89,
                33.83, 29.02, 23.11, 28.76, 41.79, 27.33, 15.79, 23.42, 28.52, 22.16, 21.34, 10.42, 10.58, 15.38, 21.31,
                27.41]
    np.asarray(old_data)
    data = get_standard_deviation_and_mean(boarding_data, n, m)
    differences = np.zeros(n, dtype=float)
    for i in range(0, n):
        differences[i] = math.fabs(old_data[i] - data[0][i])
    fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax1 = axs[0]
    ax2 = axs[1]
    ax1.errorbar(np.arange(1, n+1), data[0], yerr=data[1], fmt='go-', label='our model', ecolor='g', capthick=2)
    ax1.plot(np.arange(1, n+1), old_data, fmt='bo-', label='Beusnelink model')
    ax1.set_title('The result from our model in comparison to the one from Beusnelink')
    ax1.set_ylabel('Boarding time in minutes')
    ax2.bar(np.arange(1, n+1), differences)
    ax2.set_ylabel('Difference in mean boarding time between the two models')
    ax2.set_xlabel('Different boarding methods')
    fig.align_labels()
    plt.xticks(np.arange(1, n+1), labels, rotation='60')
    plt.show()


def figure2_two_plane_comparison(labels, boarding_data_full_bombardier, boarding_data_normal_bombardier,
                                 boarding_data_full_airbus, boarding_data_normal_airbus, n, m):
    fig, axs = plt.subplots(2, 1, sharex=True)
    ax1 = axs[0]
    ax2 = axs[1]
    data_full_airbus = get_standard_deviation_and_mean(boarding_data_full_airbus, n, m)
    data_full_bombardier = get_standard_deviation_and_mean(boarding_data_full_bombardier, n, m)
    data_normal_airbus = get_standard_deviation_and_mean(boarding_data_normal_airbus, n, m)
    data_normal_bombardier = get_standard_deviation_and_mean(boarding_data_normal_bombardier, n, m)

    ax1.errorbar(np.arange(1, n+1), data_normal_airbus[0], yerr=data_normal_airbus[1], fmt='go-',
                 label='Airbus A320-200', ecolor='g', capthick=2)
    ax1.errorbar(np.arange(1, n+1), data_normal_bombardier[0], yerr=data_normal_bombardier[1], fmt='bo-',
                 label='Bombardier CS100', ecolor='b', capthick=2)
    ax2.errorbar(np.arange(1, n+1), data_full_airbus[0], yerr=data_full_airbus[1], fmt='go-', label='Airbus A320-200',
                 ecolor='g', capthick=2)
    ax2.errorbar(np.arange(1, n+1), data_full_bombardier[0], yerr=data_full_bombardier[1], fmt='bo-',
                 label='Bombardier CS100', ecolor='b', capthick=2)

    ax1.set_title('Different Boarding Methods under two different load conditions with the Airbus A320-200 '
                  'and the Bombardier CS100')
    ax1.set_ylabel('Average boarding time in minutes for 62.4% people load and 70% luggage load')
    ax2.set_ylabel('Average boarding time in minutes for 100% people load and 100% luggage load')
    ax2.set_xlabel('Different boarding methods')
    fig.align_labels()
    plt.xticks(np.arange(1, n+1), labels, rotation='60')
    plt.show()


def figure3_two_plane_individual_times(labels, individual_boarding_data_full_bombardier_fastest_methods, individual_boarding_data_full_airbus_fastest_methods, n, m):
    fig, ax = plt.subplots()
    size = 0.35
    index = np.arange(n)

    data_individual_bombardier = get_standard_deviation_and_mean(individual_boarding_data_full_bombardier_fastest_methods,n, m)
    data_individual_airbus = get_standard_deviation_and_mean(individual_boarding_data_full_airbus_fastest_methods, n, m)

    ax.bar(index - size/2, data_individual_bombardier[0], size, yerr=data_individual_bombardier[1],
                   color='SkyBlue', label='Bombardier CS100')
    ax.bar(index + size/2, data_individual_airbus[0], size, yerr=data_individual_airbus[1],
                    color='IndianRed', label='Airbus A320-200')
    ax.set_ylabel('Average individual boarding times in minutes')
    ax.set_title('Average individual boarding times for the fastest boarding method in each category '
                 'with the Airbus A320-200 and the Bombardier CS100')
    ax.set_xticks(index)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.show()


def get_standard_deviation_and_mean(boarding_data, n, m):
    data = np.zeros((2, n), dtype=float)
    for i in range(0, n):
        mean = 0
        sd = 0
        for j in range(0, m):
            mean += boarding_data[i][j]
            sd += boarding_data[i][j] * boarding_data[i][j]
        mean /= m
        sd = math.sqrt(sd/m - (mean*mean))
        data[0][i] = mean
        data[1][i] = sd
    return data
