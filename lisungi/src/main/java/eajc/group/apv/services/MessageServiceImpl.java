package eajc.group.apv.services;

import eajc.group.apv.dto.ConversationDto;
import eajc.group.apv.dto.MessageRequestDto;
import eajc.group.apv.dto.MessageResponseDto;
import eajc.group.apv.entity.Message;
import eajc.group.apv.entity.User;
import eajc.group.apv.enums.MessageStatus;
import eajc.group.apv.exception.BadRequestException;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.mapper.MessageMapper;
import eajc.group.apv.repository.MessageRepository;
import eajc.group.apv.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
public class MessageServiceImpl implements MessageService{
    private final MessageRepository messageRepository;
    private final MessageMapper messageMapper;
    private final UserRepository userRepository;

    public MessageServiceImpl(MessageRepository messageRepository, MessageMapper messageMapper, UserRepository userRepository) {
        this.messageRepository = messageRepository;
        this.messageMapper = messageMapper;
        this.userRepository = userRepository;
    }


    @Override
    public MessageResponseDto createMessage(MessageRequestDto dto) {
        if (dto.getSenderId() == null)
            throw new BadRequestException("Expediteur introuvable.");

        if (dto.getReceiverId() == null)
            throw new BadRequestException("Bénéficiaire introuvable.");

        if (dto.getContent() == null || dto.getContent().isBlank())
            throw new BadRequestException("Le contenu est obligatoire.");

        User sender = userRepository.findById(dto.getSenderId())
                .orElseThrow(() ->
                        new ResourceNotFoundException("Expéditaire introuvable"));

        User receiver = userRepository.findById(dto.getReceiverId())
                .orElseThrow(() ->
                        new ResourceNotFoundException("Béneficiaire introuvable"));

        Message message = messageMapper.toEntity(dto, sender, receiver);

        message.setStatus(MessageStatus.SENT);

        return messageMapper.toDto(
                messageRepository.save(message)
        );
    }

    @Override
    public List<MessageResponseDto> getAllMessages() {
        return messageRepository.findAll()
                .stream()
                .map(messageMapper::toDto)
                .toList();
    }

    @Override
    public MessageResponseDto getMessageByPublicId(UUID publicId) {
        Message event = messageRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Message introvable"));
        return messageMapper.toDto(event);
    }


    @Override
    public List<ConversationDto> getConversations(Long currentUserId) {
        List<Message> messages = messageRepository.findAllConversations(currentUserId);

        Map<Long, Message> lastMessages = new LinkedHashMap<>();

        for (Message message : messages) {

            System.out.println(message +"\n");

            Long otherUserId = message.getSender().getId().equals(currentUserId)
                    ? message.getReceiver().getId()
                    : message.getSender().getId();

            lastMessages.putIfAbsent(otherUserId, message);
        }

        return lastMessages.values()
                .stream()
                .map(message -> {

                    User otherUser =
                            message.getSender().getId().equals(currentUserId)
                                    ? message.getReceiver()
                                    : message.getSender();

                    ConversationDto dto = new ConversationDto();

                    dto.setUserId(otherUser.getId());
                    dto.setUserName(otherUser.getProfile().getFirstName() + " " + otherUser.getProfile().getLastName());
                    dto.setLastMessage(message.getContent());
                    dto.setLastMessageDate(message.getSentAt());
                    dto.setUnreadCount(
                            messageRepository.countByReceiverIdAndStatus(
                                    currentUserId,
                                    MessageStatus.SENT
                            )
                    );
                    dto.setUserPhoto(otherUser.getProfile().getPhoto());

                    return dto;
                })
                .toList();
    }

    @Override
    public List<MessageResponseDto> getConversation(Long currentUserId, Long otherUserId) {
        return messageRepository
                .findConversation(currentUserId, otherUserId)
                .stream()
                .map(messageMapper::toDto)
                .toList();
    }

    @Override
    public void markConversationAsRead(Long currentUserId, Long otherUserId) {
        List<Message> messages =
                messageRepository.findConversation(currentUserId, otherUserId);

        messages.stream()
                .filter(m ->
                        m.getReceiver().getId().equals(currentUserId)
                                && m.getStatus()!=MessageStatus.READ
                )
                .forEach(m -> m.setStatus(MessageStatus.READ));

        messageRepository.saveAll(messages);
    }

    @Override
    public long countUnreadMessages(Long currentUserId) {
        return messageRepository.countByReceiverIdAndStatus(
                currentUserId,
                MessageStatus.SENT
        );
    }

    @Override
    public void deleteMessage(UUID publicId) {
        Message message = messageRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Message introuvable"));

        messageRepository.delete(message);
    }
}
