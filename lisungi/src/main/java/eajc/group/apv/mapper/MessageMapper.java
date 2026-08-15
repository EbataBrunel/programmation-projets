package eajc.group.apv.mapper;

import eajc.group.apv.dto.MessageRequestDto;
import eajc.group.apv.dto.MessageResponseDto;
import eajc.group.apv.entity.Message;
import eajc.group.apv.entity.User;
import eajc.group.apv.enums.MessageStatus;
import org.springframework.stereotype.Component;

@Component
public class MessageMapper {

    public Message toEntity(MessageRequestDto dto, User sender, User receiver){
        Message message = new Message();
        message.setSender(sender);
        message.setReceiver(receiver);
        message.setContent(dto.getContent());
        message.setStatus(MessageStatus.SENT);

        return  message;
    }

    public MessageResponseDto toDto(Message message){
        MessageResponseDto dto = new MessageResponseDto();
        dto.setPublicId(message.getPublicId());
        dto.setContent(message.getContent());
        dto.setSenderId(message.getSender().getId());
        dto.setReceiverId(message.getReceiver().getId());
        dto.setStatus(message.getStatus());
        dto.setSentAt(message.getSentAt());

        return  dto;
    }
}
