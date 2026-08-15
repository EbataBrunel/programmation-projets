package eajc.group.apv.dto;

import eajc.group.apv.enums.MessageStatus;

import java.time.LocalDateTime;
import java.util.UUID;

public class MessageResponseDto {

    private UUID publicId;

    private Long senderId;

    private Long receiverId;

    private String content;

    private MessageStatus status;

    private LocalDateTime sentAt;

    public MessageResponseDto(){}

    public MessageResponseDto(UUID publicId, Long senderId, Long receiverId, String content, MessageStatus status, LocalDateTime sentAt) {
        this.publicId = publicId;
        this.senderId = senderId;
        this.receiverId = receiverId;
        this.content = content;
        this.status = status;
        this.sentAt = sentAt;
    }


    public UUID getPublicId() {
        return publicId;
    }

    public void setPublicId(UUID publicId) {
        this.publicId = publicId;
    }

    public Long getSenderId() {
        return senderId;
    }

    public void setSenderId(Long senderId) {
        this.senderId = senderId;
    }

    public Long getReceiverId() {
        return receiverId;
    }

    public void setReceiverId(Long receiverId) {
        this.receiverId = receiverId;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public MessageStatus getStatus() {
        return status;
    }

    public void setStatus(MessageStatus status) {
        this.status = status;
    }

    public LocalDateTime getSentAt() {
        return sentAt;
    }

    public void setSentAt(LocalDateTime sentAt) {
        this.sentAt = sentAt;
    }
}
