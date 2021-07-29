from wagtail.core.blocks.field_block import ChoiceBlock


def IconFieldBlock(**kwargs):
    return ChoiceBlock(
        choices=(
            ('chat-left', 'Speech Bubble'),
            ('grap-up', 'Graph'),
            ('hammer', 'Gavel'),
        ),
        template='widgets/icon_block.html',
        **kwargs
    )
