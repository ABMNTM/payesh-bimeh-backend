from django.db import models
from django.core.exceptions import ValidationError

from core.accounts.types import EmploymentType
from core.main.models.cost_rate_rule import CostRateRule
from core.main.models.enrollment import Enrollment
from core.main.models.family_relationship import FamilyRelationship
from core.main.types import RelationshipType, SubsidyRateType


class CurrentInsuranceContract(models.Model):
    contract = models.ForeignKey(
        "main.InsuranceContract",
        models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="رکورد کنونی",
    )

    @classmethod
    def make_cost_factory(cls):
        current_contract = cls.objects.first()
        if not current_contract:
            raise ValidationError("هنوز دوره بیمه جاری ثبت نشده است.")
        cost_rules = list(
            CostRateRule.objects.filter(
                contract_id=current_contract.contract_id
            ).values(
                "employment_type", "cost_type", "subsidy_percent", "base_premium_cost"
            )
        )
        cost_factory = dict()
        for rule in cost_rules:
            employment_type = rule.pop("employment_type")
            cost_type = rule.pop("cost_type")
            cost_factory[employment_type][cost_type] = rule

        return cost_factory

    @staticmethod
    def get_cost_and_subsidy(cost_factory, employment_type, cost_type):
        if not cost_factory.get(employment_type):
            raise ValidationError(
                "خطا در محاسبه مبلغ بیمه. لطفا با پشتیبانی تماس بگیرید."
            )
        if not cost_factory[employment_type].get(cost_type):
            raise ValidationError(
                "خطا در محاسبه مبلغ بیمه. لطفا با پشتیبانی تماس بگیرید."
            )
        factory = cost_factory[employment_type][cost_type]
        return factory["base_premium_cost"], factory["subsidy_percent"]

    @classmethod
    def calculate_total_cost(cls, enrollment: Enrollment):
        cost_factory = cls.make_cost_factory()
        total_cost = 0.0
        employment_type = enrollment.guardian.employment_type
        household_head_person = enrollment.guardian.person
        for person in enrollment.covered_members.prefetch_related().all():
            if person.id == enrollment.guardian.person_id:
                cost_type = SubsidyRateType.HIRED
            else:
                try:
                    relationship = FamilyRelationship.objects.get(
                        related_person=household_head_person, person=person
                    )
                    cost_type = relationship.relationship_type
                except FamilyRelationship.DoesNotExist:
                    raise ValidationError(
                        f"شخص {person.id} ارتباط خانوادگی با شما ندارد."
                    )
            base_cost, subsidy = cls.get_cost_and_subsidy(
                cost_factory, employment_type, cost_type
            )

            # add cost to total_cost
            total_cost += base_cost * (100 - subsidy) / 100

        return total_cost
