import grpc

import course_service_pb2 as pb2
import course_service_pb2_grpc as pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pb2_grpc.CourseServiceStub(channel)

        request = pb2.GetCourseRequest(course_id="api-course")
        response = stub.GetCourse(request)

        print(response)


if __name__ == "__main__":
    run()
