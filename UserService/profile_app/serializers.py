from rest_framework import serializers
from models import Profile, Compensation, Skill, SkillId


class CompensationSerializer(serializers.ModelSerializer):
    """
    Serializer to convert Compensation object data to primitive Python Data types
    """

    class Meta:
        model = Compensation
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(CompensationSerializer, self).to_representation(instance)
        ret['compensation_id'] = ret['compensation_id'].replace('-', '')
        return ret


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

    def create(self, validated_data):
        skill, created = Skill.objects.get_or_create(**validated_data);
        return skill;

        # def to_representation(self, instance):
        #     ret = super(CompensationSerializer, self).to_representation(instance)
        #     ret['compensation_id'] = ret['compensation_id'].replace('-', '')
        #     return ret


class SkillIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillId
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer to conver Profile object data to primitive Python Data types
    """
    compensation = CompensationSerializer(many=False)

    class Meta:
        model = Profile
        fields = '__all__'

        # def create(self, validated_data):
        #     #         data is sent over like this
        #     #         JSON.stringify({
        #     #             userId: this.user.userId,
        #     #             profile:profile
        #     #         }))
        #
        #     compensation_data = validated_data.pop('compensation')
        #
        #     # create and insert compensation into db ONLY if it doesn't already exists, using "get_or_create"
        #     compensation, created = Compensation.objects.get_or_create(**compensation_data)
        #
        #     profile = Profile.objects.create(compensation=compensation, **validated_data)
        #     self.is_valid(raise_exception=True)
        #     profile.save()
        #     return profile
        #
        # def update(self, instance, validated_data):
        #     compensation_data = validated_data.pop('compensation')
        #     compensation = instance.compensation
        #
        #     instance.title = validated_data['title']
        #     instance.description = validated_data['description']
        #     instance.phone = validated_data['phone']
        #     instance.skills = validated_data['skills']
        #     instance.active = validated_data['active']
        #     instance.save()
        #
        #     compensation.amount = compensation_data['amount']
        #     compensation.duration = compensation_data['duration']
        #     compensation.save()
        #
        #     return instance
        # remove hypen from UUID
