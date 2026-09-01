import json

from json_logic import jsonLogic

from django.core.exceptions import ValidationError

from financial.models import CostRateRule, ExceptionalCondition
from main.models import Enrollment, FamilyRelationship, CurrentInsuranceContract, Person
from main.types import SubsidyRateType


class CostFactory:
    def make_cost_factory(self):
        current_contract = CurrentInsuranceContract.objects.first()
        if not current_contract:
            raise ValidationError("هنوز دوره بیمه جاری ثبت نشده است.")
        cost_rules = list(
            CostRateRule.objects.filter(
                offer__contract_id=current_contract.contract_id
            ).values(
                "id", "employment_type", "cost_type", "organ_share_percent", "base_premium_cost"
            )
        )
        cost_factory = dict()
        for rule in cost_rules:
            employment_type = rule.pop("employment_type")
            cost_type = rule.pop("cost_type")
            cost_factory[employment_type][cost_type] = rule

        return cost_factory

    def check_for_exceptional_conditions(self, rate_rule_id: int, person: Person):
        all_conditions = ExceptionalCondition.objects.filter(
            rate_rule_id=rate_rule_id, is_active=True
        ).order_by("priority")
        for exc_cond in all_conditions:
            condition = json.loads(exc_cond.condition)
            if condition and jsonLogic(condition):
                return exc_cond
        return

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
        return factory["id"], factory["base_premium_cost"], factory["organ_share_percent"]

    def calculate_total_cost(self, enrollment: Enrollment):
        cost_factory = self.make_cost_factory()
        total_cost = 0.0
        employment_type = enrollment.guardian.employment_type
        household_head_person = enrollment.guardian.person
        for person in enrollment.covered_members.prefetch_related().all():
            if person.id == household_head_person.id:
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
            rule_id, base_cost, organ_share = self.get_cost_and_subsidy(
                cost_factory, employment_type, cost_type
            )

            if exc_cond := self.check_for_exceptional_conditions(rule_id, person):
                organ_share = exc_cond.new_organ_share

            # add cost to total_cost
            total_cost += base_cost * (100 - organ_share) / 100

        return total_cost
