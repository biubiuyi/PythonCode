
def TimeStampToTime(timestamp):
    """
    时间戳转换时间
    :param timestamp:
    :return:
    """
    try:
        timeStruct = time.localtime( timestamp / 1000 )
        return time.strftime( '%Y-%m-%d %H:%M:%S', timeStruct )
    except Exception as e:
        raise Exception( 'method error: time stamp to time', e )

def missing_data(data):
    total = data.isnull().sum()
    percent = (data.isnull().sum() / data.isnull().count() * 100)
    tt = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    types = []
    for col in data.columns:
        dtype = str(data[col].dtype)
        types.append(dtype)
    tt['Types'] = types
    return (np.transpose(tt))

def plot_feature_distribution(df1, df2, label1, label2, features):
    """
    use example:
    t0 = train_df.loc[train_df['target'] == 0]
    t1 = train_df.loc[train_df['target'] == 1]
    features = train_df.columns.values[2:102]
    plot_feature_distribution(t0, t1, '0', '1', features)
    :param df1:
    :param df2:
    :param label1:
    :param label2:
    :param features:
    :return:
    """
    i = 0
    sns.set_style('whitegrid')
    plt.figure()
    fig, ax = plt.subplots(10,10,figsize=(18,22))

    for feature in features:
        i += 1
        plt.subplot(10,10,i)
        sns.distplot(df1[feature], hist=False,label=label1)
        sns.distplot(df2[feature], hist=False,label=label2)
        plt.xlabel(feature, fontsize=9)
        locs, labels = plt.xticks()
        plt.tick_params(axis='x', which='major', labelsize=6, pad=-6)
        plt.tick_params(axis='y', which='major', labelsize=6)
    plt.show();

    def get_logger():
        FORMAT = '[%(levelname)s]%(asctime)s:%(name)s:%(message)s'
        logging.basicConfig(format=FORMAT)
        logger = logging.getLogger('main')
        logger.setLevel(logging.DEBUG)
        return logger

    df['authorized_flag'].map({'Y': 1, 'N': 0})