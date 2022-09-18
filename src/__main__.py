from src.core import settings

import uvicorn


uvicorn.run(
        'src.app:app',
        host=settings.HOST,
        port=settings.PORT,
        reload=True
        )

