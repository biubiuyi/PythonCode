
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