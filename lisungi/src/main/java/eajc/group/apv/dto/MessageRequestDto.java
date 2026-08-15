package eajc.group.apv.dto;


import eajc.group.apv.enums.MessageStatus;

public class MessageRequestDto {

    private Long senderId;

    private Long receiverId;

    private String content;

    public MessageRequestDto(){}

    public MessageRequestDto(Long senderId, Long receiverId, String content) {
        this.senderId = senderId;
        this.receiverId = receiverId;
        this.content = content;
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

}
