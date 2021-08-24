from app.store.vk_api.dataclasses import Update, UpdateObject, Message


class TestHandleUpdates:
    async def test_no_messages(self, store):
        await store.bots_manager.handle_updates(updates=[])
        assert store.vk_api.send_message.called is False

    async def test_new_message(self, store):
        await store.bots_manager.handle_updates(
            updates=[
                Update(
                    type="message_new",
                    object=UpdateObject(
                        id=1,
                        user_id=1,
                        body="kek",
                    ),
                )
            ]
        )
        assert store.vk_api.send_message.call_count == 1
        message: Message = store.vk_api.send_message.mock_calls[0].args[0]
        assert message.user_id == 1
        assert message.text
