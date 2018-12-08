import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np
import math


def figure1_paper_model_vs_our_model(labels, boarding_data, n, m):
    old_data = [24.69, 27.74, 28.56, 29.80, 31.35, 30.66, 31.02, 33.77, 31.43, 30.78, 32.51, 39.80, 34.73, 29.59, 27.42,
                25.01, 27.91, 29.60, 28.30, 26.50, 29.27, 30.36, 24.75, 26.28, 25.80, 35.64, 27.23, 26.91, 50.67, 41.89,
                33.83, 29.02, 23.11, 28.76, 41.79, 27.33, 15.79, 23.42, 28.52, 22.16, 21.34, 10.42, 10.58, 15.38, 21.31,
                27.41]
    np.asarray(old_data)
    data = get_confidence_interval_and_mean(boarding_data, n, m)
    differences = np.zeros(n, dtype=float)
    for i in range(0, n):
        differences[i] = old_data[i] - data[0][i]
    plt.figure(dpi=120, figsize=(16,9))
    fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax1 = axs[0]
    ax2 = axs[1]
    ax1.errorbar(np.arange(n), data[0], yerr=data[1], fmt='go-', markersize=1.5, linewidth=0.6, label='our model', ecolor='k')
    ax1.plot(np.arange(n), old_data, 'bo-', markersize=1.5, linewidth=0.6,label='base model')
    ax1.set_ylabel('Boarding times (min)', fontsize=7)
    ax2.bar(np.arange(n), differences)
    ax2.set_ylabel('Difference in boarding times (min)', fontsize=7)
    ax1.set_ylim(bottom=0)
    ax1.axvline(x=0.5, color='k')
    ax1.axvline(x=13.5, color='k')
    ax1.axvline(x=27.5,color='k')
    ax1.axvline(x=33.5,color='k')
    ax1.axvline(x=38.5,color='k')
    ax1.axvline(x=40.5,color='k')
    ax2.axvline(x=0.5, color='k')
    ax2.axvline(x=13.5,color='k')
    ax2.axvline(x=27.5,color='k')
    ax2.axvline(x=33.5,color='k')
    ax2.axvline(x=38.5,color='k')
    ax2.axvline(x=40.5,color='k')
    ax1.legend(loc=(0.34, 0), fontsize=6, frameon=False)
    fig.align_labels()
    plt.xticks(np.arange(n), labels, fontsize=5, rotation='90')
    plt.sca(ax2)
    plt.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False, labeltop=True)
    plt.yticks(np.arange(-5, 20,2.5), fontsize=7)
    plt.sca(ax1)
    plt.xticks(np.arange(n), labels, fontsize=5, rotation='90')
    plt.yticks(np.arange(0, 60,5), fontsize=7)
    plt.subplots_adjust(hspace=1)

    plt.savefig("data/figure1/figure1.png", format='png', dpi=600)
    plt.show()


def figure2_two_plane_comparison(labels, boarding_data_full_bombardier, boarding_data_normal_bombardier,
                                 boarding_data_full_airbus, boarding_data_normal_airbus, n, m):
    plt.figure(dpi=120, figsize=(16, 9))
    fig, axs = plt.subplots(2, 1, sharex=True)
    ax1 = axs[0]
    ax2 = axs[1]
    data_full_airbus = get_confidence_interval_and_mean(boarding_data_full_airbus, n, m)
    data_full_bombardier = get_confidence_interval_and_mean(boarding_data_full_bombardier, n, m)
    data_normal_airbus = get_confidence_interval_and_mean(boarding_data_normal_airbus, n, m)
    data_normal_bombardier = get_confidence_interval_and_mean(boarding_data_normal_bombardier, n, m)

    ax1.errorbar(np.arange(n), data_normal_airbus[0], yerr=data_normal_airbus[1], fmt='o-', color='SkyBlue', markersize=1.5,
                 linewidth=0.6, label='Airbus A320-200', ecolor='k', capthick=2)
    ax1.errorbar(np.arange(n), data_normal_bombardier[0], yerr=data_normal_bombardier[1], fmt='o-',color='IndianRed',
                 markersize=1.5, linewidth=0.6, label='Bombardier CS100', ecolor='k', capthick=2)
    ax2.errorbar(np.arange(n), data_full_airbus[0], yerr=data_full_airbus[1], fmt='o-',color='SkyBlue',
                 markersize=1.5, linewidth=0.6, label='Airbus A320-200', ecolor='k', capthick=2)
    ax2.errorbar(np.arange(n), data_full_bombardier[0], yerr=data_full_bombardier[1], fmt='o-',color='IndianRed',
                 markersize=1.5, linewidth=0.6, label='Bombardier CS100', ecolor='k', capthick=2)

    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)
    ax1.axvline(x=0.5, color='k')
    ax1.axvline(x=13.5, color='k')
    ax1.axvline(x=27.5, color='k')
    ax1.axvline(x=33.5, color='k')
    ax1.axvline(x=38.5, color='k')
    ax1.axvline(x=40.5, color='k')
    ax1.axvline(x=45.5, color='k')
    ax2.axvline(x=0.5, color='k')
    ax2.axvline(x=13.5, color='k')
    ax2.axvline(x=27.5, color='k')
    ax2.axvline(x=33.5, color='k')
    ax2.axvline(x=38.5, color='k')
    ax2.axvline(x=40.5, color='k')
    ax2.axvline(x=45.5, color='k')
    ax1.set_ylabel('Average boarding time (min) \n 62.5% people load and 70% luggage load', fontsize=7)
    ax1.legend(loc=(0.34, 0), fontsize=6, frameon=False)
    ax2.set_ylabel('Average boarding time (min) \n 100% people load and 100% luggage load', fontsize=7)
    ax2.legend(loc=(0.34, 0), fontsize=6, frameon=False)
    fig.align_labels()
    plt.xticks(np.arange(n), labels, fontsize=5, rotation='90')
    plt.sca(ax2)
    plt.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False, labeltop=True)
    plt.yticks(np.arange(0, 60, 5), fontsize=7)
    plt.sca(ax1)
    plt.xticks(np.arange(n), labels, fontsize=5, rotation='90')
    plt.yticks(np.arange(0, 30, 5), fontsize=7)
    plt.subplots_adjust(hspace=1)

    plt.savefig("data/figure2/figure2.png", format='png', dpi=600)
    plt.show()


def figure3_two_plane_individual_times(labels, chosen, individual_boarding_data_full_bombardier, individual_boarding_data_full_airbus, n, m):
    fig, ax = plt.subplots()
    size = 0.35
    index = np.arange(len(chosen))

    data_individual_bombardier = get_confidence_interval_and_mean(individual_boarding_data_full_bombardier, n, m)
    data_individual_airbus = get_confidence_interval_and_mean(individual_boarding_data_full_airbus, n, m)
    data_individual_bombardier_best = np.zeros((2, len(chosen)), dtype=float)
    data_individual_airbus_best = np.zeros((2, len(chosen)), dtype=float)
    chosen_labels = []
    i = 0
    for j in range(0, n):
        if i < len(chosen) and chosen[i] == j:
            data_individual_bombardier_best[0][i] = data_individual_bombardier[0][j]
            data_individual_bombardier_best[1][i] = data_individual_bombardier[1][j]
            data_individual_airbus_best[0][i] = data_individual_airbus[0][j]
            data_individual_airbus_best[1][i] = data_individual_airbus[1][j]
            chosen_labels.append(labels[j])
            i += 1

    ax.bar(index - size/2, data_individual_bombardier_best[0], size, yerr=data_individual_bombardier_best[1],
                   color='IndianRed', label='Bombardier CS100')
    ax.bar(index + size/2, data_individual_airbus_best[0], size, yerr=data_individual_airbus_best[1],
                    color='SkyBlue', label='Airbus A320-200')
    ax.set_ylabel('Average individual boarding times (min)')
    plt.xticks(index, chosen_labels, fontsize=6, rotation='90')
    ax.legend(loc=0, fontsize=6, frameon=False)
    plt.subplots_adjust(hspace=1)
    #plt.gcf().subplots_adjust(bottom=0.3)
    plt.tight_layout()
    plt.savefig("data/figure3/figure3.png", format='png', dpi=600)
    plt.show()


def figure4_effect_of_luggage_on_times(labels, boarding_data_random, boarding_data_steffen, n, m):
    data_random = get_confidence_interval_and_mean(boarding_data_random, n, m)
    data_steffen = get_confidence_interval_and_mean(boarding_data_steffen, n, m)
    fix, ax = plt.subplots()
    ax.errorbar(np.arange(n), data_random[0], yerr=data_random[1], fmt='go', markersize=2.5, label='Random', ecolor='g')
    ax.errorbar(np.arange(n), data_steffen[0], yerr=data_steffen[1], fmt='bo', markersize=2.5, label='Steffen', ecolor='b')
    ax.set_xticks(np.arange(n))
    ax.set_xticklabels(labels)
    ax.legend(loc=2, fontsize=10, frameon=False)
    ax.set_ylabel('Boarding times (min)', fontsize=12)
    ax.set_xlabel('Luggage load as a percentage of total capacity (%)', fontsize=12)
    plt.savefig("data/figure4/figure4.png", format='png', dpi=600)
    plt.show()


def get_confidence_interval_and_mean(boarding_data, n, m):
    # 95% confidence interval z = 1.96
    z = 1.96
    data = np.zeros((3, n), dtype=float)
    for i in range(0, n):
        mean = 0
        sd = 0
        for j in range(0, m):
            mean += boarding_data[i][j]
            sd += boarding_data[i][j] * boarding_data[i][j]
        mean /= m
        sd = math.sqrt(sd/m - (mean*mean))
        data[0][i] = mean
        data[1][i] = z * sd / math.sqrt(m)
        data[2][i] = sd
    return data


def get_figure_1():
    a = np.loadtxt('data/figure1/total_data_old_plane.txt', delimiter=',')
    times_total = np.zeros((46, 5), dtype=float)
    times_individual = np.zeros((46, 5), dtype=float)
    labels_list = []
    f = open("test_methods.txt", "r+")
    lines = f.readlines()
    for i in range(0, 46):
        for j in range(0, 5):
            times_total[i][j] = a[i][j]
            times_individual[i][j] = a[i][j+5]
        line = lines[i].split()
        labels_list.append(line[0])
    f.close()
    figure1_paper_model_vs_our_model(labels_list, times_total, 46, 5)


def get_figure_2():
    a = np.loadtxt('data/figure2/times_load_70_passengers_625_plane_1_total.csv', delimiter=',')
    b = np.loadtxt('data/figure2/times_load_70_passengers_625_plane_2_total.csv', delimiter=',')
    c = np.loadtxt('data/figure2/times_load_100_passengers_100_plane_1_total.csv', delimiter=',')
    d = np.loadtxt('data/figure2/times_load_100_passengers_100_plane_2_total.csv', delimiter=',')
    labels_list = []
    f = open("test_methods.txt", "r+")
    lines = f.readlines()
    for i in range(0, 49):
        line = lines[i].split()
        labels_list.append(line[0])
    f.close()
    figure2_two_plane_comparison(labels_list, c, a, d, b, 49, 5)


def get_figure_3():
    a = np.loadtxt('data/figure3/times_load_100_passengers_100_plane_1_individual.csv', delimiter=',')
    b = np.loadtxt('data/figure3/times_load_100_passengers_100_plane_2_individual.csv', delimiter=',')
    labels_list = []
    chosen = [0, 1, 22, 31, 36, 40, 43, 46]
    f = open("test_methods.txt", "r+")
    lines = f.readlines()
    for i in range(0, 49):
        line = lines[i].split()
        labels_list.append(line[0])
    f.close()
    figure3_two_plane_individual_times(labels_list, chosen, a, b, 49, 5)

def get_figure_4():
    random = np.loadtxt('data/figure4/loads_random.csv', delimiter=',')
    steffen = np.loadtxt('data/figure4/loads_steffen.csv', delimiter=',')
    labels = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

    figure4_effect_of_luggage_on_times(labels, random, steffen, 21, 5)


get_figure_2()
