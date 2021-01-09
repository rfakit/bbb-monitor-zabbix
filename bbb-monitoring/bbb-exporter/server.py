import logging
import sys, json
from time import sleep


import settings
from collector import BigBlueButtonCollector
from helpers import verify_recordings_base_dir_exists

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s]: %(message)s")

if __name__ == '__main__':
    if settings.DEBUG:
        logging.getLogger().setLevel(logging.DEBUG)

    if settings.RECORDINGS_METRICS_READ_FROM_DISK:
        logging.info("Enabling recordings metrics read from disk, we will not request expensive recordings metrics "
                     "via the API")
        if verify_recordings_base_dir_exists():
            logging.debug("BigBlueButton recordings base dir exists")
        else:
            logging.fatal("BigBlueButton recordings base dir (" + settings.recordings_metrics_base_dir + ") does not " +
                          "exist. Disable RECORDINGS_METRICS_READ_FROM_DISK=true or run on BigBlueButton server.")
            sys.exit(1)

    # start_http_server(settings.PORT, addr=settings.BIND_IP)
    # logging.info("HTTP server started on port: {}".format(settings.PORT))

    collector = BigBlueButtonCollector()

    if len(settings.ROOM_PARTICIPANTS_CUSTOM_BUCKETS) > 0:
        collector.set_room_participants_buckets(settings.ROOM_PARTICIPANTS_CUSTOM_BUCKETS)

    if len(settings.ROOM_LISTENERS_CUSTOM_BUCKETS) > 0:
        collector.set_room_listeners_buckets(settings.ROOM_LISTENERS_CUSTOM_BUCKETS)

    if len(settings.ROOM_VOICE_PARTICIPANTS_CUSTOM_BUCKETS) > 0:
        collector.set_room_voice_participants_buckets(settings.ROOM_VOICE_PARTICIPANTS_CUSTOM_BUCKETS)

    if len(settings.ROOM_VIDEO_PARTICIPANTS_CUSTOM_BUCKETS) > 0:
        collector.set_room_video_participants_buckets(settings.ROOM_VIDEO_PARTICIPANTS_CUSTOM_BUCKETS)

    # REGISTRY.register(collector)
    desc_func = collector.collect
    # for metric in desc_func():
    #     print(metric)
    type_suffixes = {
        'counter': ['_total', '_created'],
        'summary': ['', '_sum', '_count', '_created'],
        'histogram': ['_sum', '_count', '_created'],
        'gaugehistogram': ['_gsum', '_gcount'],
        'info': ['_info'],
    }

    result = []
    outstr = ''
    for metric in desc_func():
        for suffix in type_suffixes.get(metric.type, ['']):
            result.append(metric.name + suffix)
        # print (json.dumps(result, indent=4))

        for s in metric.samples:
            if s.name in result:
                stmp = s.name
                stmp += '_' + s.labels['type'] if 'type' in s.labels else ''
                if 'parameters' in s.labels and '=' in s.labels['parameters']:
                    stmp += '_' + s.labels['parameters'].split('=')[1]
                # print(s.name + '_' + s.labels['type'] if 'type' in s.labels else s.name, s.value)
                print(stmp, s.value)
                outstr = outstr + stmp + ' ' + str(s.value) + '\n'
                # print(s)
            # pass
        f = open(settings.OUTPUT_PATH, "w")
        f.write(outstr)
        f.close()

