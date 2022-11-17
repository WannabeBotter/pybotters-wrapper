from __future__ import annotations

import pandas as pd

from pybotters import bitbankDataStore
from pybotters_wrapper.bitbank import bitbankWebsocketChannels
from pybotters_wrapper.common import (
    DataStoreWrapper,
    TickerStore,
    TradesStore,
    OrderbookStore,
)


class bitbankTickerStore(TickerStore):
    def _normalize(self, d: dict, op: str) -> "TickerItem":
        return self._itemize(d["pair"], float(d["last"]))


class bitbankTradesStore(TradesStore):
    def _normalize(self, d: dict, op: str) -> "TradesItem":
        return self._itemize(
            str(d["transaction_id"]),
            d["pair"],
            d["side"].upper(),
            float(d["price"]),
            float(d["amount"]),
            pd.to_datetime(d["executed_at"]),
        )


class bitbankOrderbookStore(OrderbookStore):
    def _normalize(self, d: dict, op: str) -> "OrderbookItem":
        return self._itemize(
            d["pair"], d["side"].upper(), float(d["price"]), float(d["size"])
        )


class bitbankDataStoreWrapper(DataStoreWrapper[bitbankDataStore]):
    _WRAP_STORE = bitbankDataStore
    _WEBSOCKET_CHANNELS = bitbankWebsocketChannels
    _TICKER_STORE = (bitbankTickerStore, "ticker")
    _TRADES_STORE = (bitbankTradesStore, "transactions")
    _ORDERBOOK_STORE = (bitbankOrderbookStore, "depth")

    async def connect(
        self,
        client: "pybotters.Client",
        *,
        endpoint: str = None,
        send: any = None,
        hdlr: "WsStrHandler" | "WsBytesHandler" = None,
        waits: list["DataStore" | str] = None,
        send_type: str = "json",
        hdlr_type: str = "json",
        auto_reconnect: bool = False,
        on_reconnection: "Callable" = None,
        **kwargs,
    ) -> dict[str, "WebSocketRunner"]:
        return await super().connect(
            client,
            endpoint=endpoint,
            send=send,
            hdlr=hdlr,
            waits=waits,
            send_type="str",
            hdlr_type="str",
            auto_reconnect=auto_reconnect,
            on_reconnection=on_reconnection,
            **kwargs,
        )