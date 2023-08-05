import celery
import time


app = celery.Celery()


@app.task(bind=True)
def hello(self, a, b):
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 50})
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 90})
    time.sleep(1)
    return 'hello world: %i' % (a+b)


def on_raw_message(body):
    print(body)

r = hello.apply_async(4, 5)
print(type(r))
print(r.get(on_message=on_raw_message, propagate=False))

