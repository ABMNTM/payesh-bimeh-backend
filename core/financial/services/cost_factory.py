import json

from django.db.models import OuterRef, Subquery
from json_logic import jsonLogic
from decimal import Decimal

from django.core.exceptions import ValidationError

from accounts.models.user import User
from financial.models import CostRateRule, ExceptionalCondition
from main.models import CurrentInsuranceContract, Person
from main.types import SubsidyRateType, Gender, VeteranStatus


class CostRateRuleServices:
    def __init__(self):
        self.cost_factory = self.make_cost_factory()

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
            if employment_type not in cost_factory:
                cost_factory[employment_type] = dict()
            cost_factory[employment_type][cost_type] = rule

        return cost_factory

    def check_for_exceptional_conditions(self, rate_rule_id: int, person: Person):
        all_conditions = ExceptionalCondition.objects.filter(
            rate_rule_id=rate_rule_id, is_active=True
        ).order_by("priority")

        conditions_context = self.build_person_context(person)

        for exc_cond in all_conditions:
            if jsonLogic(exc_cond.condition, conditions_context):
                return exc_cond
        return

    def get_cost_and_subsidy(self, employment_type, cost_type):
        if not self.cost_factory.get(employment_type):
            raise ValidationError(
                "خطا در محاسبه مبلغ بیمه. لطفا با پشتیبانی تماس بگیرید."
            )
        if not self.cost_factory[employment_type].get(cost_type):
            raise ValidationError(
                "خطا در محاسبه مبلغ بیمه. لطفا با پشتیبانی تماس بگیرید."
            )
        factory = self.cost_factory[employment_type][cost_type]
        return factory["id"], factory["base_premium_cost"], factory["organ_share_percent"]

    @staticmethod
    def convert_to_decimal(*nums):
        return tuple(map(lambda x: Decimal(str(x)), nums))

    def build_person_context(self, person: Person):
        required_attrs = [
            "birth_day",
            "birth_month",
            "birth_year",
            "birth_place",
            "gender",
            "is_household_head",
            "deployed_unit",
            "organizational_unit",
            "veteran_status",
        ]
        return {
            "person": {
                **{
                    attr: getattr(person, attr) for attr in required_attrs
                },
                "household": {
                    attr: getattr(person.household, attr)
                    for attr in required_attrs
                } if person.household else None
            },
            "gender": {
                "male": Gender.MALE.value,
                "female": Gender.FEMALE.value,
            },
            "veteran_status": {
                "veteran": VeteranStatus.VETERAN.value,
                "disabled": VeteranStatus.DISABLED.value,
                "martyr_spouse": VeteranStatus.MARTYR_SPOUSE.value,
                "martyr_child": VeteranStatus.MARTYR_CHILD.value,
                "former_pow": VeteranStatus.FORMER_POW.value,
                "none": VeteranStatus.NONE.value,
            }
        }


class CostFactory:
    def __init__(self):
        self.cost_service = CostRateRuleServices()

    def calculate_total_cost(self, guardian: User, members):
        total_cost = Decimal("0")
        employment_type_id = guardian.employment_type.id
        household_head_person = guardian.person
        all_covered_members = members.select_related("household")
        total_cost += self.get_person_cost(
            household_head_person, employment_type_id, is_household=True
        )
        for person in all_covered_members:
            cost = self.get_person_cost(person, employment_type_id)
            # add cost to total_cost
            total_cost += cost

        return total_cost

    def get_person_cost(self, person, employment_type_id, is_household=False):
        if is_household:
            cost_type = SubsidyRateType.HIRED
        else:
            cost_type = person.relationship
        rule_id, base_cost, organ_share = self.cost_service.get_cost_and_subsidy(
            employment_type_id, cost_type
        )

        if exc_cond := self.cost_service.check_for_exceptional_conditions(rule_id, person):
            organ_share = exc_cond.new_organ_share

        base_cost, organ_share = self.cost_service.convert_to_decimal(base_cost, organ_share)

        return base_cost * (Decimal("100") - organ_share) / Decimal("100")


def calculate_total_cost(guardian: User, members):
    cost_factory = CostFactory()
    return cost_factory.calculate_total_cost(guardian, members)
