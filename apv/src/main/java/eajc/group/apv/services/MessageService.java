package eajc.group.apv.services;

import eajc.group.apv.dto.ConversationDto;
import eajc.group.apv.dto.MessageRequestDto;
import eajc.group.apv.dto.MessageResponseDto;

import java.util.List;
import java.util.UUID;

public interface MessageService {

    // CREATE
    MessageResponseDto createMessage(MessageRequestDto dto);

    // READ
    List<MessageResponseDto> getAllMessages();

    // GET
    MessageResponseDto getMessageByPublicId(UUID publicId);

    // GET
    List<ConversationDto> getConversations(Long currentUserId);

    // GET
    public List<MessageResponseDto> getConversation(Long currentUserId, Long otherUserId);

    // GET
    void markConversationAsRead(Long currentUserId, Long otherUserId);

    // GET
    public long countUnreadMessages(Long currentUserId);

    // DELETE
    void deleteMessage(UUID publicId);

}
