function vertex(n) 
{
    return  [2*Math.cos(n * Math.PI/3.0 + Math.PI/6.0),
             2*Math.sin(n * Math.PI/3.0 + Math.PI/6.0)];
}

hex = [];
for (var i = 0; i < 6; i++) {
        hex.push(vertex(i));
}

function move(co, nudge)
{
        r = [];
        xx = nudge[0];
        yy = nudge[1];
        for (let i = 0; i < 6; i++) {
                x = co[i][0];
                y = co[i][1];
                r.push([x+xx, y+yy]);
        }			
        return r;
} 

function cordsToHex(center) 
{
        hex = [];
        for (var i = 0; i < 6; i++) {
                hex.push(vertex(i));
        }
                return move(hex, center);
}

function draw(hex)
{

        var ctx = canvas.getContext('2d');


        ctx.beginPath();
        ctx.moveTo(hex[0][0], hex[0][1]);
        ctx.lineTo(hex[1][0], hex[1][1]);
        ctx.lineTo(hex[2][0], hex[2][1]);
        ctx.lineTo(hex[3][0], hex[3][1]);
        ctx.lineTo(hex[4][0], hex[4][1]);
        ctx.lineTo(hex[5][0], hex[5][1]);
        ctx.closePath();
        ctx.fill(); 
}

function pic(i)
{
        var ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        co = cords[i];

        for (var j = 0; j < (co.length); j++) {
                draw(cordsToHex(co[j]));
        }
}

pic(5);










