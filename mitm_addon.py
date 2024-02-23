import logging

from mitmproxy import ctx, http, version


class ToggleBlock:
    def request(self, flow: http.HTTPFlow) -> None:
        req = flow.request
        logging.info(f"Inspecting {req.path=}...")
        if req.path == "/wifi/off":
            logging.info(f"Intercepted: {req.path=}")
            # !~u /wifi/(on|off)$ -> alone isn't enough since bryt.in urls were passing through
            ctx.options.set(r"block_list=:~all & !~u /wifi/(on|off)$:444", r"block_list=:~d .*\.bryt\.in:444")
            flow.response = http.Response.make(200, content="off", headers={"Server": version.MITMPROXY})
        elif req.path == "/wifi/on":
            logging.info(f"Intercepted: {req.path=}")
            ctx.options._options["block_list"].reset()
            ctx.options.changed.send(updated={"block_list"})  # required for notifying all listeners
            flow.response = http.Response.make(200, content="on", headers={"Server": version.MITMPROXY})


addons = [ToggleBlock()]
