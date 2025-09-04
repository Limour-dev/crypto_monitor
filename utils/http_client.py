from utils.logger import logger
import os
import urllib.request
import urllib.error
import urllib.parse
# ==================== 配置代理 ====================

proxy = os.getenv('PROXY', '').strip()
if proxy:
    # 定义代理
    proxy = {
        'http': proxy,
        'https': proxy,
    }
    # 构建代理处理器
    proxy_handler = urllib.request.ProxyHandler(proxy)
    # 构建一个 opener
    opener = urllib.request.build_opener(proxy_handler)
else:
    opener = urllib.request.urlopen

# ==================== HTTP 客户端  ====================

import time, json
from typing import Any, Dict, Optional

# 默认配置
DEFAULT_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 1.0
BACKOFF_FACTOR = 1.5

class HttpClient:
    """
    通用 HTTP 客户端
    """

    def __init__(self, base_url: str = "", timeout: int = DEFAULT_TIMEOUT, max_retries: int = MAX_RETRIES):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

    def _build_url(self, url: str) -> str:
        if url.startswith("http://") or url.startswith("https://"):
            return url
        return f"{self.base_url}/{url.lstrip('/')}" if self.base_url else url

    def request(self, method: str, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        method = method.upper()
        url = self._build_url(url)

        timeout = kwargs.get("timeout", self.timeout)
        headers = kwargs.get("headers", {})
        data = kwargs.get("data", None)
        params = kwargs.get("params", None)  # 新增

        if params:
            if isinstance(params, dict):
                query_str = urllib.parse.urlencode(params)
            else:
                query_str = str(params)
            # 如果 URL 已经有 ?，追加 &，否则加 ?
            url += ("&" if "?" in url else "?") + query_str

        # 如果是 dict，转成 bytes
        if isinstance(data, dict):
            data = json.dumps(data).encode("utf-8")
            headers.setdefault("Content-Type", "application/json")

        for attempt in range(self.max_retries + 1):
            try:
                req = urllib.request.Request(url=url, data=data, headers=headers, method=method)
                with opener.open(req, timeout=timeout) as resp:
                    status_code = resp.getcode()
                    resp_text = resp.read().decode("utf-8", errors="replace")

                if status_code < 400:
                    try:
                        return json.loads(resp_text)
                    except Exception as e:
                        logger.warning(f"无法解析 JSON 响应: {e}")
                        return {"raw": resp_text}

                if status_code < 500:
                    logger.error(f"{method} {url} → {status_code}: {resp_text}")
                    return None
                else:
                    logger.warning(f"服务端错误 {status_code}，准备重试...")

            except urllib.error.HTTPError as e:
                # HTTPError 是 URLError 的子类
                status_code = e.code
                body = e.read().decode("utf-8", errors="replace")
                if status_code < 500:
                    logger.error(f"{method} {url} → {status_code}: {body}")
                    return None
                else:
                    logger.warning(f"服务端错误 {status_code}，准备重试...")

            except urllib.error.URLError as e:
                logger.error(f"请求失败: {url} | {e}")

            if attempt < self.max_retries:
                delay = RETRY_DELAY * (BACKOFF_FACTOR ** attempt)
                time.sleep(delay)
                logger.warning(f"重试 {attempt + 1}/{self.max_retries} → {url}")
            else:
                logger.error(f"达到最大重试次数，请求失败: {url}")

        return None

    def get(self, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        return self.request("POST", url, **kwargs)

# ====================
# 全局 HTTP 客户端实例
# ====================
http_client = HttpClient(timeout=10, max_retries=3)