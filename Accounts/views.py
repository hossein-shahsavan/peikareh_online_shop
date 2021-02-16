from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from .serializers import CreateUserSerializer, LoginUserSerializer, UserSerializer, ForgetPasswordSerializer, \
    AddressSerializer

from .permissions import IsOwner

from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import login
from rest_auth.views import LoginView as RestLoginView
from .models import User, PhoneOTP, Address
from random import randint
from kavenegar import *
from rest_framework.views import APIView


class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = (IsOwner,)


class UserIDView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'userID': request.user.id}, status=HTTP_200_OK)


class AddressListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = (AddressSerializer,)

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class AddressCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class AddressUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class AddressDeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Address.objects.all()


class Login(RestLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)
        return super().post(request, format=None)


class ValidatePhoneSendOTP(APIView):
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({'detail': 'Phone Number already exists'}, status=HTTP_400_BAD_REQUEST)
                # logic to send the otp and store the phone number and that otp in table.
            else:
                otp = randint(9999, 99999)

                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if not old:
                        count = count + 1

                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=otp,
                            Count=count,

                        )
                        sendOTP(phone, otp)

                    else:
                        count = old[0].Count
                        old[0].Count = count + 1
                        old[0].otp = otp
                        old[0].save()
                        sendOTP(phone, otp)

                    if count > 4:
                        return Response({
                            'detail': 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        },
                            status=HTTP_500_INTERNAL_SERVER_ERROR
                        )


                else:
                    return Response({
                        'status': 'False', 'detail': "OTP sending error. Please try after some time."
                    }, status=HTTP_400_BAD_REQUEST
                    )

                return Response({
                    'status': True, 'detail': 'Otp has been sent successfully.'
                }, status=HTTP_200_OK
                )
        else:
            return Response({
                'status': 'False', 'detail': "I haven't received any phone number. Please do a POST request."
            }, status=HTTP_400_BAD_REQUEST
            )


def sendOTP(phone, otp):
    api = KavenegarAPI(
        '43524A676D5230483251434F3533366A58623232456A522B6D786634746654464F4756426A45584C374C773D')
    params = {'receptor': phone,
              'template': 'verification',
              'token': otp,
              'type': 'sms vs call'
              }
    response = api.verify_lookup(params)


class ValidateOTP(APIView):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password

    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()

                    return Response({
                        'status': True,
                        'detail': 'OTP matched, Please proceed to save password'
                    }, status=HTTP_200_OK
                    )
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect, please try again'
                    }, status=HTTP_400_BAD_REQUEST
                    )
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone not recognised. Please request a new otp with this number'
                }, status=HTTP_400_BAD_REQUEST
                )


        else:
            return Response({
                'status': 'False',
                'detail': 'Either phone or otp was not recieved in Post request'
            }, status=HTTP_400_BAD_REQUEST
            )


class Register(APIView):
    '''Takes phone and a password and creates a new user only if otp was verified and phone is new'''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)

        if phone and password:
            phone = str(phone)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({'status': False,
                                 'detail': 'Phone Number already have account associated. Kindly try forgot password'},
                                status=HTTP_400_BAD_REQUEST)
            else:
                old = PhoneOTP.objects.filter(phone__iexact=phone)
                if old.exists():
                    old = old.first()
                    if old.logged:
                        Temp_data = {'phone': phone, 'password': password}

                        serializer = CreateUserSerializer(data=Temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        user.save()

                        old.delete()
                        return Response({
                            'status': True,
                            'detail': 'Congrats, user has been created successfully.'
                        }, status=HTTP_200_OK
                        )

                    else:
                        return Response({
                            'status': False,
                            'detail': 'Your otp was not verified earlier. Please go back and verify otp'

                        }, status=HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response({
                        'status': False,
                        'detail': 'Phone number not recognised. Kindly request a new otp with this number'
                    }, status=HTTP_400_BAD_REQUEST
                    )





        else:
            return Response({
                'status': 'False',
                'detail': 'Either phone or password was not recieved in Post request'
            }, status=HTTP_400_BAD_REQUEST
            )


class ValidatePhoneForgotPassword(APIView):
    '''
    Validate if account is there for a given phone number and then send otp for forgot password reset'''

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                otp = randint(9999, 99999)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if not old:
                        count = count + 1

                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=otp,
                            Count=count,
                            forgot=True,
                        )
                        send_OTP_forget(phone, otp)
                        return Response({'status': True, 'detail': 'OTP has been sent for password reset'},
                                        status=HTTP_200_OK)

                    else:
                        if old[0].Count >= 3:
                            return Response({
                                'status': False,
                                'detail': 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                            }, status=HTTP_500_INTERNAL_SERVER_ERROR
                            )
                        else:
                            count = old[0].Count
                            old[0].Count = count + 1
                            old[0].otp = otp
                            old[0].save()
                            send_OTP_forget(phone, otp)
                            return Response(
                                {'status': True,
                                 'detail': 'OTP has been sent for password reset. Limits about to reach.'},
                                status=HTTP_200_OK)

                else:
                    return Response({
                        'status': 'False', 'detail': "OTP sending error. Please try after some time."
                    }, status=HTTP_400_BAD_REQUEST
                    )
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone number not recognised. Kindly try a new account for this number'
                }, status=HTTP_400_BAD_REQUEST)


def send_OTP_forget(phone, otp):
    api = KavenegarAPI(
        '43524A676D5230483251434F3533366A58623232456A522B6D786634746654464F4756426A45584C374C773D')
    params = {'receptor': phone,
              'template': 'ResetPassword',
              'token': otp,
              'type': 'sms vs call'
              }
    response = api.verify_lookup(params)


class ValidateOTPForgetPassword(APIView):
    '''
    If you have received an otp, post a request with phone and that otp and you will be redirected to reset  the forgotted password

    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old[0]
                if not old.forgot:
                    return Response({
                        'status': False,
                        'detail': 'This phone havenot send valid otp for forgot password. Request a new otp or contact help centre.'
                    }, status=HTTP_400_BAD_REQUEST
                    )

                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.forgot_logged = True
                    old.save()

                    return Response({
                        'status': True,
                        'detail': 'OTP matched, kindly proceed to create new password'
                    }, status=HTTP_200_OK)
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect, please try again'
                    }, status=HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone not recognised. Kindly request a new otp with this number'
                }, status=HTTP_400_BAD_REQUEST
                )

        else:
            return Response({
                'status': 'False',
                'detail': 'Either phone or otp was not recieved in Post request'
            }, status=HTTP_400_BAD_REQUEST)


class ForgetPasswordChange(APIView):
    '''
    if forgot_logged is valid and account exists then only pass otp, phone and password to reset the password. All three should match.APIView
    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp = request.data.get("otp", False)
        password = request.data.get('password', False)

        if phone and otp and password:
            old = PhoneOTP.objects.filter(Q(phone__iexact=phone) & Q(otp__iexact=otp))
            if old.exists():
                old = old.first()
                if old.forgot_logged:
                    post_data = {
                        'phone': phone,
                        'password': password
                    }
                    user_obj = get_object_or_404(User, phone__iexact=phone)
                    serializer = ForgetPasswordSerializer(data=post_data)
                    serializer.is_valid(raise_exception=True)
                    if user_obj:
                        user_obj.set_password(serializer.data.get('password'))
                        user_obj.active = True
                        user_obj.save()
                        old.delete()
                        return Response({
                            'status': True,
                            'detail': 'Password changed successfully. Please Login'
                        },status=HTTP_200_OK)

                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP Verification failed. Please try again in previous step'
                    }, status=HTTP_400_BAD_REQUEST)

            else:
                return Response({
                    'status': False,
                    'detail': 'Phone and otp are not matching or a new phone has entered. Request a new otp in forgot password'
                }, status=HTTP_400_BAD_REQUEST)

        else:
            return Response({
                'status': False,
                'detail': 'Post request have parameters missing.'
            }, status=HTTP_400_BAD_REQUEST)
