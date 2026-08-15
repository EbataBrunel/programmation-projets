package eajc.group.apv.dto;

import eajc.group.apv.enums.MessageStatus;

import java.time.LocalDateTime;
import java.util.UUID;

public class ConversationDto {
    private Long userId;

    private String userName;

    private String lastMessage;

    private LocalDateTime lastMessageDate;

    private long unreadCount;

    private MessageStatus status;

    private String userPhoto;

    public ConversationDto(){};

    public ConversationDto(Long userId, String userName, String lastMessage, LocalDateTime lastMessageDate, long unreadCount, MessageStatus status, String userPhoto) {
        this.userId = userId;
        this.userName = userName;
        this.lastMessage = lastMessage;
        this.lastMessageDate = lastMessageDate;
        this.unreadCount = unreadCount;
        this.status = status;
        this.userPhoto = userPhoto;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getLastMessage() {
        return lastMessage;
    }

    public void setLastMessage(String lastMessage) {
        this.lastMessage = lastMessage;
    }

    public LocalDateTime getLastMessageDate() {
        return lastMessageDate;
    }

    public void setLastMessageDate(LocalDateTime lastMessageDate) {
        this.lastMessageDate = lastMessageDate;
    }

    public long getUnreadCount() {
        return unreadCount;
    }

    public void setUnreadCount(long unreadCount) {
        this.unreadCount = unreadCount;
    }

    public MessageStatus getStatus() {
        return status;
    }

    public void setStatus(MessageStatus status) {
        this.status = status;
    }

    public String getUserPhoto() {
        return userPhoto;
    }

    public void setUserPhoto(String userPhoto) {
        this.userPhoto = userPhoto;
    }
}
