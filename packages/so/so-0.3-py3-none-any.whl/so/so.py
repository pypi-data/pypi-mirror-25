import click
import logging



APP_DESC = """
    _____                                ______ __  __
    |  __ \                              |  ____|  \/  |
    | |  | | __ _ _ __  _ __ ___  _   _  | |__  | \  / |
    | |  | |/ _` | '_ \| '_ ` _ \| | | | |  __| | |\/| |
    | |__| | (_| | | | | | | | | | |_| |_| |    | |  | |
    |_____/ \__,_|_| |_|_| |_| |_|\__,_(_)_|    |_|  |_|

                        ---- A Terminal Tools For DouyuTV

    @author Alexander Luo (496952252@qq.com)
                                    last_update 2017-07-10 08:54:59
"""



def main():
    print(APP_DESC)
    parse_command()





def parse_command(quality, mode, path, thread, verbose, url):
    """
指定获取主播的房间地址对主播直播情况进行抓取与统计 (Mac and Ubuntu Only)

Example:

    danmu.fm -q 2 -v 1 http://www.douyu.com/qiuri

    danmu.fm -q 3 -m 0 -p "videos/20160609_1900_2240_小苍.mp4" -v 1 http://www.douyu.com/qiuri

    """

    # danmu.fm -q 3 -m 0 -p "videos/20160609_1900_2240_小苍.mp4"-v 1 http://www.douyu.com/qiuri
    # config["video_quality"] = quality if quality > -1 or quality < 4 else 0
    # config["danmu_mode"] = mode if mode > -1 and mode < 2 else 0
    # current_working_dir = os.getcwd()
    # config["video_stored_path"] = os.path.join(current_working_dir,path) if path != "." else current_working_dir
    # config["thread_num"] = thread if thread >= 2 or mode <= 50 else 10
    # config["verbose"] = verbose
    # # [TODO:如果等于1就普通,如果为4直接开启全局日志]
    # config["zhubo_room_url"] = url
    # logger.info("正在检查环境")
    # check_setting_and_env()
    # logger.info("环境检查完毕,正在开启斗鱼客户端(请等待15s~30s)")
    # start_douyu_client()













@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)


@click.command()
@click.option('--spring', type=click.Choice(['boot', 'mvc']))    # 限定值
def choose(spring):
    click.echo('spring: %s' % spring)

if __name__ == '__main__':
    main()
    choose()
    hello()