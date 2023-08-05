from .bridge import AioBridge
from .light import AioLight
from .group import AioGroup, AioAllLights


Bridge = AioBridge
Light = AioLight
Group = AioGroup
AllLights = AioAllLights


def main():
    import argparse
    import logging

    import phue

    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True)
    parser.add_argument('--config-file-path', required=False)
    args = parser.parse_args()

    while True:
        try:
            b = AioBridge(args.host, config_file_path=args.config_file_path)
            break
        except phue.PhueRegistrationException as e:
            input("Press button on Bridge then hit Enter to try again")


if __name__ == '__main__':
    main()
