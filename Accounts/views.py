from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK

from .serializers import CreateUserSerializer, LoginUserSerializer, UserSerializer, ForgetPasswordSerializer, AddressSerializer

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
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class AddressUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class AddressDeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
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
                return Response({'status': False, 'detail': 'Phone Number already exists'})
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
                        sendOTP(otp, phone=None)

                    else:
                        count = old[0].Count
                        old[0].Count = count + 1
                        old[0].otp = otp
                        old[0].save()
                        sendOTP(otp, phone=None)

                    if count > 7:
                        return Response({
                            'status': False,
                            'detail': 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        })


                else:
                    return Response({
                        'status': 'False', 'detail': "OTP sending error. Please try after some time."
                    })

                return Response({
                    'status': True, 'detail': 'Otp has been sent successfully.'
                })
        else:
            return Response({
                'status': 'False', 'detail': "I haven't received any phone number. Please do a POST request."
            })


def sendOTP(otp, phone=None):
    api = KavenegarAPI(
        '7351315847785361446D6F6C39744E582F56503434687043676E375251366C3564553968784435554653773D')
    params = {'receptor': '09220489835',
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
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone not recognised. Please request a new otp with this number'
                })


        else:
            return Response({
                'status': 'False',
                'detail': 'Either phone or otp was not recieved in Post request'
            })


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
                                 'detail': 'Phone Number already have account associated. Kindly try forgot password'})
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
                            'detail': 'Congrts, user has been created successfully.'
                        })

                    else:
                        return Response({
                            'status': False,
                            'detail': 'Your otp was not verified earlier. Please go back and verify otp'

                        })
                else:
                    return Response({
                        'status': False,
                        'detail': 'Phone number not recognised. Kindly request a new otp with this number'
                    })





        else:
            return Response({
                'status': 'False',
                'detail': 'Either phone or password was not recieved in Post request'
            })


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
                        send_OTP_forget(otp, phone=None)
                        return Response({'status': True, 'detail': 'OTP has been sent for password reset'})

                    else:
                        if old[0].Count >= 3:
                            return Response({
                                'status': False,
                                'detail': 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                            })
                        else:
                            count = old[0].Count
                            old[0].Count = count + 1
                            old[0].otp = otp
                            old[0].save()
                            send_OTP_forget(otp, phone=None)
                            return Response(
                                {'status': True,
                                 'detail': 'OTP has been sent for password reset. Limits about to reach.'})

                else:
                    return Response({
                        'status': 'False', 'detail': "OTP sending error. Please try after some time."
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone number not recognised. Kindly try a new account for this number'
                })


def send_OTP_forget(otp, phone=None):
    api = KavenegarAPI(
        '7351315847785361446D6F6C39744E582F56503434687043676E375251366C3564553968784435554653773D')
    params = {'receptor': '09220489835',
              'template': 'verification',
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
                    })

                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.forgot_logged = True
                    old.save()

                    return Response({
                        'status': True,
                        'detail': 'OTP matched, kindly proceed to create new password'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone not recognised. Kindly request a new otp with this number'
                })

        else:
            return Response({
                'status': 'False',
                'detail': 'Either phone or otp was not recieved in Post request'
            })


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
                        })

                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP Verification failed. Please try again in previous step'
                    })

            else:
                return Response({
                    'status': False,
                    'detail': 'Phone and otp are not matching or a new phone has entered. Request a new otp in forgot password'
                })

        else:
            return Response({
                'status': False,
                'detail': 'Post request have parameters mising.'
            })
