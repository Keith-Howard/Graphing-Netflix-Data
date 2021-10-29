import matplotlib
import pandas as pd
import matplotlib.pyplot as plt


def df_from_contained_data(dataframe, column_label, column_data):
    return dataframe[dataframe[column_label].str.contains(column_data, regex=False)]


def df_from_time(dataframe, column_label, operator, days, hours, minutes, seconds):
    time_data = days + ' days ' + hours + ':' + minutes + ':' + seconds
    if operator == '>':
        filtered_time = dataframe[(dataframe[column_label] > time_data)]
    elif operator == '>=':
        filtered_time = dataframe[(dataframe[column_label] >= time_data)]
    elif operator == '<=':
        filtered_time = dataframe[(dataframe[column_label] <= time_data)]
    else:
        filtered_time = dataframe[(dataframe[column_label] < time_data)]
    return filtered_time


def sum_df_column(dataframe, column_label):
    return dataframe[column_label].sum()


def set_graph_characteristics(figure, axis_coordinates, x_values, y_values, bar_width, title, font_size):
    matplotlib.rcParams.update({'font.size': font_size})
    ax = figure.add_axes(axis_coordinates)
    ax.bar(x_values, y_values, width=bar_width)
    ax.set_title(title)


def get_values_by_category_column(dafaframe, category_label):
    daily_view_count = dafaframe[category_label].value_counts()
    sorted_view_count = daily_view_count.sort_index()
    return sorted_view_count.values


def add_weekday_and_category_column_labels(dataframe):
    days_of_week = ['0 Monday', '1 Tuesday', '2 Wednesday', '3 Thursday', '4 Friday', '5 Saturday', '6 Sunday']
    dataframe.loc[:, 'weekday num and day'] = dataframe['Start Time'].dt.weekday .astype(str) + ' ' + \
                                              dataframe['Start Time'].dt.day_name()
    dataframe.loc[:, 'weekday categories'] = pd.Categorical(dataframe['weekday num and day'],
                                                            categories=days_of_week, ordered=True)


netflix_activity_file = r"input/ViewingActivity.csv"
df = pd.read_csv(netflix_activity_file)
df = df.drop(['Profile Name', 'Attributes', 'Supplemental Video Type',
              'Device Type', 'Bookmark', 'Latest Bookmark', 'Country'], axis=1)
df['Start Time'] = pd.to_datetime(df['Start Time'], utc=False)

selected_archer = df_from_contained_data(df, 'Title', 'Archer').copy()
selected_archer.loc[:, 'Duration Delta'] = pd.to_timedelta(selected_archer['Duration'])
archer_show_duration = df_from_time(selected_archer, 'Duration Delta', '>=', '0', '00', '01', '00').copy()
time_spent_watching_archer = sum_df_column(archer_show_duration, 'Duration Delta')

selected_office = df_from_contained_data(df, 'Title', 'The Office (U.S.)').copy()
selected_office.loc[:, 'Duration Delta'] = pd.to_timedelta(selected_office['Duration'])
office_show_duration = df_from_time(selected_office, 'Duration Delta', '>=', '0', '00', '01', '00').copy()
time_spent_watching_office = sum_df_column(archer_show_duration, 'Duration Delta')

add_weekday_and_category_column_labels(office_show_duration)
add_weekday_and_category_column_labels(archer_show_duration)

days_of_week_label = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
fig = plt.figure(figsize=(8, 7))
fig.suptitle('Netflix Data Graph')
set_graph_characteristics(fig, [0.08, 0.10, 0.85, 0.30], days_of_week_label,
                          get_values_by_category_column(archer_show_duration, 'weekday categories'), .45,
                          'Archer Episodes Watched by Day\n', 9)
set_graph_characteristics(fig, [0.08, 0.55, 0.85, 0.30], days_of_week_label,
                          get_values_by_category_column(office_show_duration, 'weekday categories'), .45,
                          'Office Episodes Watched by Day\n', 9)
plt.show()
