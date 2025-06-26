from aiohttp import web
import json
import asyncio
import random
from datetime import datetime

async def handle_request(request):
    """处理所有HTTP请求"""
    try:
        # 获取基本请求信息
        method = request.method
        path = request.path_qs
        
        # 尝试获取请求体
        try:
            if request.content_length and request.content_length > 0:
                body = await request.text()
            else:
                body = ""
        except:
            body = ""
        
        
        # 构建简单的请求信息
        request_info = {
            "method": method,
            "path": path,
            "body": body,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "accepted": "true"
        }
        
        # 构建响应内容
        response_content = f"{json.dumps(request_info, ensure_ascii=False)}"
        
        # 记录请求
        print(f"[{request_info['timestamp']}] {method} {path}")
        if body:
            print(f"Body: {body}")
        
        # 处理完请求后随机sleep 10-30秒
        sleep_time = random.randint(10, 30)
        print(f"[INFO] Request processed, sleeping for {sleep_time} seconds...")
        await asyncio.sleep(sleep_time)
        print(f"[INFO] Sleep completed, sending response.")
        
        return web.Response(
            text=response_content,
            status=200,
            content_type='text/plain'
        )
        
    except Exception as e:
        print(f"Error: {e}")
        error_response = f"{{\"error\": \"{str(e)}\", \"timestamp\": \"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\"}}"
        
        # 错误处理后也随机sleep 10-30秒
        sleep_time = random.randint(10, 30)
        print(f"[INFO] Error handled, sleeping for {sleep_time} seconds...")
        await asyncio.sleep(sleep_time)
        print(f"[INFO] Sleep completed, sending error response.")
        
        return web.Response(
            text=error_response,
            status=200,
            content_type='text/plain'
        )

def create_app():
    """创建应用"""
    app = web.Application()
    app.router.add_route('*', '/{path:.*}', handle_request)
    return app

if __name__ == "__main__":
    app = create_app()
    
    print("=" * 50)
    print("🚀 Simple HTTP Server Starting...")
    print("📡 Listening on: http://localhost:8000")
    print("🔄 Response format: 'accepted+' + request details")
    print("💡 Press Ctrl+C to stop")
    print("=" * 50)
    
    web.run_app(app, host='localhost', port=8000) 